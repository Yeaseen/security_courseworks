import torch
import torch.nn as nn
from torch.distributions.categorical import Categorical
from torch.optim import Adam
import numpy as np
import gymnasium as gym
from gymnasium.spaces import Discrete, Box
import matplotlib.pyplot as plt
import time

def mlp(sizes, activation=nn.Tanh, output_activation=nn.Identity):
    layers = []
    for j in range(len(sizes)-1):
        act = activation if j < len(sizes)-2 else output_activation
        layers += [nn.Linear(sizes[j], sizes[j+1]), act()]
    return nn.Sequential(*layers)

def train(env_name='CartPole-v1', hidden_sizes=[64], lr=5e-3, 
          epochs=50, batch_size=5000, render=False):

    print(f"Training with environment: {env_name}")
    print(f"Hidden sizes: {hidden_sizes}, Learning rate: {lr}, "
          f"Epochs: {epochs}, Batch size: {batch_size}, Render: {render}\n")
    
    # Main training environment (no human rendering here).
    env = gym.make(env_name)
    assert isinstance(env.observation_space, Box), \
        "This example only works for envs with continuous state spaces."
    assert isinstance(env.action_space, Discrete), \
        "This example only works for envs with discrete action spaces."

    obs_dim = env.observation_space.shape[0]
    n_acts = env.action_space.n

    # Create a second environment for visualization (human render).
    eval_env = gym.make(env_name, render_mode='human')

    # Policy network.
    logits_net = mlp(sizes=[obs_dim] + hidden_sizes + [n_acts])

    def get_policy(obs):
        logits = logits_net(obs)
        return Categorical(logits=logits)

    # Action selection with no gradient updates (test-time).
    def get_action_no_grad(obs):
        with torch.no_grad():
            logits = logits_net(obs)
            return Categorical(logits=logits).sample().item()

    # Action selection with gradient-tracking (training-time).
    def get_action(obs):
        return get_policy(obs).sample().item()

    def compute_loss(obs, act, weights):
        logp = get_policy(obs).log_prob(act)
        return -(logp * weights).mean()

    optimizer = Adam(logits_net.parameters(), lr=lr)

    epoch_returns = []
    epoch_losses = []

    def train_one_epoch():
        batch_obs = []
        batch_acts = []
        batch_weights = []
        batch_rets = []
        batch_lens = []

        obs, info = env.reset()
        done = False
        ep_rews = []

        finished_rendering_this_epoch = False

        while True:
            if (not finished_rendering_this_epoch) and render:
                env.render()

            batch_obs.append(obs.copy())
            act = get_action(torch.as_tensor(obs, dtype=torch.float32))
            obs, rew, terminated, truncated, info = env.step(act)
            done = terminated or truncated
            batch_acts.append(act)
            ep_rews.append(rew)

            if done:
                ep_ret = sum(ep_rews)
                ep_len = len(ep_rews)
                batch_rets.append(ep_ret)
                batch_lens.append(ep_len)
                batch_weights += [ep_ret] * ep_len

                obs, info = env.reset()
                done = False
                ep_rews = []
                finished_rendering_this_epoch = True

                if len(batch_obs) > batch_size:
                    break

        optimizer.zero_grad()
        batch_loss = compute_loss(
            obs=torch.as_tensor(batch_obs, dtype=torch.float32),
            act=torch.as_tensor(batch_acts, dtype=torch.int32),
            weights=torch.as_tensor(batch_weights, dtype=torch.float32)
        )
        batch_loss.backward()
        optimizer.step()
        return batch_loss, batch_rets, batch_lens

    def watch_agent():
        """Render one episode with the current policy (eval_env)."""
        obs, info = eval_env.reset()
        done = False
        total_rew = 0
        while not done:
            # Sleep to slow down the rendering if desired.
            time.sleep(0.02)  
            action = get_action_no_grad(torch.as_tensor(obs, dtype=torch.float32))
            obs, rew, terminated, truncated, info = eval_env.step(action)
            done = terminated or truncated
            total_rew += rew
        print(f"Rendered policy: Episode Return = {total_rew}")

    for i in range(epochs):
        batch_loss, batch_rets, batch_lens = train_one_epoch()
        avg_ret = np.mean(batch_rets)
        avg_len = np.mean(batch_lens)
        epoch_returns.append(avg_ret)
        epoch_losses.append(batch_loss.item())

        print(f"Epoch {i:3d} | Loss: {batch_loss:.3f} | "
              f"Avg Return: {avg_ret:.3f} | "
              f"Avg Episode Length: {avg_len:.3f} | "
              f"Episodes: {len(batch_rets)}")

        # Render one rollout from the current policy at the end of each epoch.
        # You can remove or comment this out if it’s too slow.
        watch_agent()

    # Plotting the training performance.
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(epoch_returns, marker='o')
    plt.xlabel("Epoch")
    plt.ylabel("Average Return")
    plt.title("Policy Gradient Performance (Return)")

    plt.subplot(1, 2, 2)
    plt.plot(epoch_losses, marker='o', color='r')
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Policy Gradient Loss Over Time")

    plt.tight_layout()
    plt.savefig("P1b_pg_cartpole_performance.png")
    plt.show()

    # Close the rendering environment after training.
    eval_env.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--env_name', '--env', type=str, default='CartPole-v1')
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--lr', type=float, default=5e-3)
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--batch_size', type=int, default=5000)
    args = parser.parse_args()
    print('\nUsing updated policy gradient implementation with additional logging and post-epoch rendering.\n')
    train(env_name=args.env_name, render=args.render, lr=args.lr, epochs=args.epochs, batch_size=args.batch_size)

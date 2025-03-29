import torch
import torch.nn as nn
from torch.distributions.categorical import Categorical
from torch.optim import Adam
import numpy as np
import gymnasium as gym
from gymnasium.spaces import Box, Discrete
import matplotlib.pyplot as plt

def mlp(sizes, activation=nn.Tanh, output_activation=nn.Identity):
    # Build a feedforward neural network.
    layers = []
    for j in range(len(sizes)-1):
        act = activation if j < len(sizes)-2 else output_activation
        layers += [nn.Linear(sizes[j], sizes[j+1]), act()]
    return nn.Sequential(*layers)

def train_reward_to_go(env_name='CartPole-v1', hidden_sizes=[32], lr=1e-2, 
                       epochs=50, batch_size=5000, render=False, seed=0):
    """
    Train a policy using reward-to-go returns instead of full-episode returns.
    """
    print(f"\nTraining Reward-to-Go PG on {env_name} (seed={seed})")
    print(f"Hidden sizes: {hidden_sizes}, LR: {lr}, Epochs: {epochs}, Batch size: {batch_size}\n")

    # Set random seed for reproducibility.
    torch.manual_seed(seed)
    np.random.seed(seed)

    env = gym.make(env_name)
    assert isinstance(env.observation_space, Box), "Continuous state space required."
    assert isinstance(env.action_space, Discrete), "Discrete action space required."

    obs_dim = env.observation_space.shape[0]
    n_acts = env.action_space.n

    # Build policy network.
    logits_net = mlp(sizes=[obs_dim] + hidden_sizes + [n_acts])

    # Action distribution.
    def get_policy(obs):
        logits = logits_net(obs)
        return Categorical(logits=logits)

    # Sample action with gradient tracking.
    def get_action(obs):
        return get_policy(obs).sample().item()

    # Reward-to-go loss.
    def compute_loss(obs, act, weights):
        logp = get_policy(obs).log_prob(act)
        return -(logp * weights).mean()

    optimizer = Adam(logits_net.parameters(), lr=lr)

    # For logging
    epoch_returns = []
    epoch_lengths = []
    epoch_losses = []
    total_timesteps = 0  # track total steps for plotting

    def train_one_epoch():
        nonlocal total_timesteps

        batch_obs = []
        batch_acts = []
        batch_weights = []  # now these will be reward-to-go returns
        batch_rets = []
        batch_lens = []

        obs, info = env.reset()
        done = False
        ep_rews = []

        while True:
            if render:
                env.render()

            batch_obs.append(obs.copy())
            act = get_action(torch.as_tensor(obs, dtype=torch.float32))
            obs, rew, terminated, truncated, info = env.step(act)
            done = terminated or truncated
            ep_rews.append(rew)
            batch_acts.append(act)
            total_timesteps += 1

            if done:
                ep_ret = sum(ep_rews)
                ep_len = len(ep_rews)
                batch_rets.append(ep_ret)
                batch_lens.append(ep_len)

                # -------------------------
                # Key Difference:
                # For each step t in the episode, assign the sum of rewards from t to the end
                for t in range(ep_len):
                    rtg = sum(ep_rews[t:])
                    batch_weights.append(rtg)
                # -------------------------

                obs, info = env.reset()
                done = False
                ep_rews = []

                # End experience collection if batch is big enough
                if len(batch_obs) > batch_size:
                    break

        # Compute and take a gradient step.
        optimizer.zero_grad()
        batch_loss = compute_loss(
            obs=torch.as_tensor(batch_obs, dtype=torch.float32),
            act=torch.as_tensor(batch_acts, dtype=torch.int32),
            weights=torch.as_tensor(batch_weights, dtype=torch.float32)
        )
        batch_loss.backward()
        optimizer.step()

        return batch_loss.item(), batch_rets, batch_lens

    for epoch in range(epochs):
        batch_loss, batch_rets, batch_lens = train_one_epoch()
        epoch_returns.append(np.mean(batch_rets))
        epoch_lengths.append(np.mean(batch_lens))
        epoch_losses.append(batch_loss)

        print(f"Epoch {epoch:3d} | Loss: {batch_loss:.3f} | "
              f"AvgReturn: {epoch_returns[-1]:.3f} | "
              f"AvgEpLen: {epoch_lengths[-1]:.1f} | "
              f"Timesteps: {total_timesteps}")

    env.close()

    return {
        'returns': epoch_returns,
        'losses': epoch_losses,
        'lengths': epoch_lengths
    }

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--env_name', type=str, default='CartPole-v1')
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--lr', type=float, default=1e-2)
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--batch_size', type=int, default=5000)
    parser.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()

    results = train_reward_to_go(env_name=args.env_name,
                                 hidden_sizes=[32],
                                 lr=args.lr,
                                 epochs=args.epochs,
                                 batch_size=args.batch_size,
                                 render=args.render,
                                 seed=args.seed)

    # Simple plot of results
    plt.figure(figsize=(10,4))
    plt.subplot(1,2,1)
    plt.plot(results['returns'], label='Reward-to-Go')
    plt.xlabel('Epoch')
    plt.ylabel('Average Return')
    plt.title('RTG Policy Gradient Performance')
    plt.legend()

    plt.subplot(1,2,2)
    plt.plot(results['losses'], label='Loss', color='red')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('RTG Policy Gradient Loss')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('P2_pg_reward_to_go.png')
    plt.show()

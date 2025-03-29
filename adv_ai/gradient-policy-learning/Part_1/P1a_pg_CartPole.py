import torch
import torch.nn as nn
from torch.distributions.categorical import Categorical
from torch.optim import Adam
import numpy as np
import gymnasium as gym
from gymnasium.spaces import Discrete, Box
import matplotlib.pyplot as plt

def mlp(sizes, activation=nn.Tanh, output_activation=nn.Identity):
    # Build a feedforward neural network.
    layers = []
    for j in range(len(sizes)-1):
        act = activation if j < len(sizes)-2 else output_activation
        layers += [nn.Linear(sizes[j], sizes[j+1]), act()]
    return nn.Sequential(*layers)

def train(env_name='CartPole-v1', hidden_sizes=[64], lr=5e-3, 
          epochs=50, batch_size=5000, render=False):

    # Print out the chosen hyperparameters for clarity.
    print(f"Training with environment: {env_name}")
    print(f"Hidden sizes: {hidden_sizes}, Learning rate: {lr}, Epochs: {epochs}, Batch size: {batch_size}, Render: {render}\n")
    
    # Create environment and verify that its observation and action spaces are appropriate.
    env = gym.make(env_name)
    assert isinstance(env.observation_space, Box), \
        "This example only works for envs with continuous state spaces."
    assert isinstance(env.action_space, Discrete), \
        "This example only works for envs with discrete action spaces."

    obs_dim = env.observation_space.shape[0]
    n_acts = env.action_space.n

    # Build the policy network.
    logits_net = mlp(sizes=[obs_dim] + hidden_sizes + [n_acts])

    # Define a function to get the action distribution.
    def get_policy(obs):
        logits = logits_net(obs)
        return Categorical(logits=logits)

    # Define a function to select an action.
    def get_action(obs):
        return get_policy(obs).sample().item()

    # Define the loss function.
    def compute_loss(obs, act, weights):
        logp = get_policy(obs).log_prob(act)
        return -(logp * weights).mean()

    # Set up the optimizer.
    optimizer = Adam(logits_net.parameters(), lr=lr)

    # Lists to store metrics for plotting.
    epoch_returns = []
    epoch_losses = []
    epoch_episode_counts = []

    def train_one_epoch():
        # Initialize lists for experience logging.
        batch_obs = []          # Observations
        batch_acts = []         # Actions
        batch_weights = []      # Weights (cumulative reward per episode)
        batch_rets = []         # Episode returns
        batch_lens = []         # Episode lengths

        # Reset the environment.
        obs, info = env.reset()  
        done = False            
        ep_rews = []           

        finished_rendering_this_epoch = False

        while True:
            # Render if desired (only for the first episode of each epoch).
            if (not finished_rendering_this_epoch) and render:
                env.render()

            # Save the current observation.
            batch_obs.append(obs.copy())

            # Sample an action.
            act = get_action(torch.as_tensor(obs, dtype=torch.float32))
            obs, rew, terminated, truncated, info = env.step(act)
            done = terminated or truncated

            # Save action and reward.
            batch_acts.append(act)
            ep_rews.append(rew)

            if done:
                # When the episode ends, compute its return and length.
                ep_ret = sum(ep_rews)
                ep_len = len(ep_rews)
                batch_rets.append(ep_ret)
                batch_lens.append(ep_len)
                
                # Print details every 10 episodes.
                if len(batch_rets) % 10 == 0:
                    print(f"  Episode {len(batch_rets):3d}: Return = {ep_ret:.2f}, Length = {ep_len}")

                # Use the total return as the weight for every step in the episode.
                batch_weights += [ep_ret] * ep_len

                # Reset the episode.
                obs, info = env.reset()
                done, ep_rews = False, []
                finished_rendering_this_epoch = True

                # End the batch when we've collected enough observations.
                if len(batch_obs) > batch_size:
                    break

        # Perform a single policy gradient update.
        optimizer.zero_grad()
        batch_loss = compute_loss(
            obs=torch.as_tensor(batch_obs, dtype=torch.float32),
            act=torch.as_tensor(batch_acts, dtype=torch.int32),
            weights=torch.as_tensor(batch_weights, dtype=torch.float32)
        )
        batch_loss.backward()
        optimizer.step()
        return batch_loss, batch_rets, batch_lens

    # Main training loop.
    for i in range(epochs):
        batch_loss, batch_rets, batch_lens = train_one_epoch()
        avg_ret = np.mean(batch_rets)
        avg_len = np.mean(batch_lens)
        epoch_returns.append(avg_ret)
        epoch_losses.append(batch_loss.item())
        epoch_episode_counts.append(len(batch_rets))
        print(f"Epoch {i:3d} | Loss: {batch_loss:.3f} | Avg Return: {avg_ret:.3f} | Avg Episode Length: {avg_len:.3f} | Episodes: {len(batch_rets)}")
    
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
    plt.savefig("P1a_pg_cartpole_performance.png")
    plt.show()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--env_name', '--env', type=str, default='CartPole-v1')
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--lr', type=float, default=5e-3)
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--batch_size', type=int, default=5000)
    args = parser.parse_args()
    print('\nUsing updated policy gradient implementation with additional logging and plotting.\n')
    train(env_name=args.env_name, render=args.render, lr=args.lr, epochs=args.epochs, batch_size=args.batch_size)


import os
import sys
# Add the parent directory to sys.path so we can import core.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import numpy as np
import torch
import torch.nn as nn
from torch.optim import Adam
import gymnasium as gym
import matplotlib.pyplot as plt

# Import the MLPActorCritic class from core.py.
from core import MLPActorCritic

def train_pg(env_name, hidden_sizes, lr, epochs, batch_size, seed):
    """
    Trains a policy using a simple policy gradient algorithm with the
    MLPActorCritic architecture. Works for both discrete and continuous action spaces.
    We use the full-episode return method (each timestep’s weight equals the episode return).
    """
    print(f"\n=== Training on {env_name} (seed={seed}) ===")
    torch.manual_seed(seed)
    np.random.seed(seed)

    env = gym.make(env_name)
    obs_dim = env.observation_space.shape[0]
    
    # Determine appropriate dtype for actions.
    if isinstance(env.action_space, gym.spaces.Discrete):
        act_dtype = torch.long
    else:
        act_dtype = torch.float32

    # Build actor-critic model using core.py.
    ac = MLPActorCritic(env.observation_space, env.action_space, 
                        hidden_sizes=hidden_sizes, activation=nn.Tanh)
    optimizer = Adam(ac.parameters(), lr=lr)

    epoch_returns = []
    epoch_losses = []
    total_timesteps = 0

    def train_one_epoch():
        nonlocal total_timesteps

        batch_obs = []
        batch_acts = []
        batch_weights = []  # Weight for each timestep (here: full episode return)
        batch_rets = []
        batch_lens = []

        obs, info = env.reset()
        done = False
        ep_rews = []

        while True:
            # Save the current observation.
            batch_obs.append(obs.copy())
            
            # Get action using the policy (we use the step() method from core.py)
            # Since ac.step expects a tensor, convert the observation.
            obs_tensor = torch.as_tensor(obs, dtype=torch.float32)
            a, _, _ = ac.step(obs_tensor)  # ignore value and logp outputs here
            # For discrete spaces, 'a' will be a numpy scalar; for continuous, an array.
            batch_acts.append(a)
            
            obs, rew, terminated, truncated, info = env.step(a.item() if isinstance(a, np.ndarray) == False else a)
            done = terminated or truncated
            ep_rews.append(rew)
            total_timesteps += 1

            if done:
                ep_ret = sum(ep_rews)
                ep_len = len(ep_rews)
                batch_rets.append(ep_ret)
                batch_lens.append(ep_len)
                # Every timestep in the episode is weighted by the full episode return.
                batch_weights += [ep_ret] * ep_len

                obs, info = env.reset()
                done = False
                ep_rews = []

                if len(batch_obs) > batch_size:
                    break

        # Convert collected data to tensors.
        obs_tensor = torch.as_tensor(np.array(batch_obs), dtype=torch.float32)
        acts_tensor = torch.as_tensor(np.array(batch_acts), dtype=act_dtype)
        weights_tensor = torch.as_tensor(np.array(batch_weights), dtype=torch.float32)

        # Compute the log probabilities for the actions using the actor part.
        _, logp = ac.pi(obs_tensor, acts_tensor)
        loss = -(logp * weights_tensor).mean()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        return loss.item(), batch_rets, batch_lens

    for epoch in range(epochs):
        batch_loss, batch_rets, batch_lens = train_one_epoch()
        avg_ret = np.mean(batch_rets)
        epoch_returns.append(avg_ret)
        epoch_losses.append(batch_loss)
        print(f"Epoch {epoch:3d} | Loss: {batch_loss:.3f} | AvgReturn: {avg_ret:.3f} | Timesteps: {total_timesteps}")

    env.close()
    return {'returns': epoch_returns, 'losses': epoch_losses}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--env_name', type=str, default='CartPole-v1',
                        help="Environment name. For example: 'CartPole-v1' (discrete) or 'InvertedPendulum-v2' (continuous).")
    parser.add_argument('--lr', type=float, default=1e-2)
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--batch_size', type=int, default=5000)
    parser.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()

    # Train policy gradient with the general-purpose actor-critic model.
    results = train_pg(env_name=args.env_name,
                       hidden_sizes=[32],
                       lr=args.lr,
                       epochs=args.epochs,
                       batch_size=args.batch_size,
                       seed=args.seed)

    # Generate a unique filename based on env_name (replace '-' with '_' for file name compatibility)
    file_env_name = args.env_name.replace("-", "_")

    # Plot Average Return and Loss over epochs.
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(results['returns'], marker='o')
    plt.xlabel("Epoch")
    plt.ylabel("Average Return")
    plt.title(f"Return vs. Epoch ({args.env_name})")
    
    plt.subplot(1, 2, 2)
    plt.plot(results['losses'], marker='o', color='red')
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title(f"Loss vs. Epoch ({args.env_name})")
    
    plt.tight_layout()
    save_filename = f"pg_general_performance_{file_env_name}.png"
    plt.savefig(save_filename)
    print(f"Figure saved as {save_filename}")
    plt.show()

if __name__ == '__main__':
    main()

import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Set up the LunarLander environment
env = gym.make("LunarLander-v3")

# Training Parameters
num_episodes = 1000
reward_log = []

# Training Loop using a Random Policy
for episode in tqdm(range(num_episodes), desc="Training Random Policy"):
    state, _ = env.reset()
    total_reward = 0
    done = False
    
    while not done:
        action = env.action_space.sample()  # Randomly select an action
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        total_reward += reward
    
    reward_log.append(total_reward)

# Plot Learning Curve
rolling_length = 50
reward_moving_average = np.convolve(reward_log, np.ones(rolling_length) / rolling_length, mode='valid')
plt.figure(figsize=(12, 5))
plt.title("Random Policy Learning Curve - Lunar Lander")
plt.xlabel("Episode")
plt.ylabel("Average Reward")
plt.plot(reward_moving_average, label='Random Policy Moving Average Reward')
plt.legend()
plt.tight_layout()
plt.savefig("random_policy_lunar_lander.png")

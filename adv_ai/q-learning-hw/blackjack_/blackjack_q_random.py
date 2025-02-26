from __future__ import annotations

from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from tqdm import tqdm

import gymnasium as gym


env = gym.make('Blackjack-v1', natural=False, sab=False)

done = False
observation, info = env.reset()

action = env.action_space.sample()
print(action)
observation, reward, terminated, truncated, info = env.step(action)
print(observation, reward, terminated, truncated, info)


class BlackjackAgent:
    def __init__(
        self,
        env,
        learning_rate: float,
        initial_epsilon: float,
        epsilon_decay: float,
        final_epsilon: float,
        discount_factor: float = 0.95,
    ):
        self.q_values = defaultdict(lambda: np.zeros(env.action_space.n))

        self.lr = learning_rate
        self.discount_factor = discount_factor

        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon

        self.training_error = []

    def get_action(self, env, obs: tuple[int, int, bool]) -> int:
        # with probability epsilon return a random action to explore the environment
        if np.random.random() < self.epsilon:
            return env.action_space.sample()

        # with probability (1 - epsilon) act greedily (exploit)
        else:
            return int(np.argmax(self.q_values[obs]))

    def update(
        self,
        obs: tuple[int, int, bool],
        action: int,
        reward: float,
        terminated: bool,
        next_obs: tuple[int, int, bool],
    ):
        """Updates the Q-value of an action."""
        future_q_value = (not terminated) * np.max(self.q_values[next_obs])
        temporal_difference = (
            reward + self.discount_factor * future_q_value - self.q_values[obs][action]
        )

        self.q_values[obs][action] = (
            self.q_values[obs][action] + self.lr * temporal_difference
        )
        self.training_error.append(temporal_difference)

    def decay_epsilon(self):
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)



# hyperparameters
learning_rate = 0.01
n_episodes = 100_000
start_epsilon = 1.0
epsilon_decay = start_epsilon / (n_episodes / 2)  # reduce the exploration over time
final_epsilon = 0.1

agent = BlackjackAgent(
    env=env,
    learning_rate=learning_rate,
    initial_epsilon=start_epsilon,
    epsilon_decay=epsilon_decay,
    final_epsilon=final_epsilon,
)

env = gym.wrappers.RecordEpisodeStatistics(env, buffer_length=n_episodes)
for episode in tqdm(range(n_episodes), desc="Q-Learning"):
    obs, info = env.reset()
    done = False

    # play one episode
    while not done:
        action = agent.get_action(env, obs)
        next_obs, reward, terminated, truncated, info = env.step(action)

        # update the agent
        agent.update(obs, action, reward, terminated, next_obs)

        # update if the environment is done and the current obs
        done = terminated or truncated
        obs = next_obs

    agent.decay_epsilon()


rolling_length = 5000
reward_data = np.array(env.return_queue)  # Directly use the float values from the queue

# Compute the moving average of rewards
reward_moving_average = np.convolve(reward_data, np.ones(rolling_length) / rolling_length, mode='valid')

# Create the plot
fig, axs = plt.subplots(figsize=(12, 5))
axs.set_title("Q-Learning Curve Plot")
axs.set_xlabel("Episode")
axs.set_ylabel("Average Reward")
axs.plot(reward_moving_average, label='Moving Average of Rewards')
axs.legend()

# Tight layout for better spacing
plt.tight_layout()

# Save the figure
plt.savefig("Q_learning_curve_plot.png")



# Simulate random policy
random_rewards = []
for episode in tqdm(range(n_episodes), desc="Random Policy"):
    obs, info = env.reset()
    done = False
    total_reward = 0

    while not done:
        action = env.action_space.sample()  # Choose action randomly
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        done = terminated or truncated

    random_rewards.append(total_reward)




# Settings for the plot
rolling_length = 5000
reward_data = np.array(env.return_queue)  # Directly use the float values from the queue

# Compute the moving average of rewards
reward_moving_average = np.convolve(reward_data, np.ones(rolling_length) / rolling_length, mode='valid')

# Create the plot
fig, axs = plt.subplots(figsize=(12, 5))
axs.set_title("Random Policy Curve Plot")
axs.set_xlabel("Episode")
axs.set_ylabel("Average Reward")
axs.plot(reward_moving_average, label='Moving Average of Rewards')
axs.legend()

# Tight layout for better spacing
plt.tight_layout()

# Save the figure
plt.savefig("random_policy_learning_curve_plot.png")



# rolling_length = 500
# fig, axs = plt.subplots(ncols=1, figsize=(12, 5))
# axs.set_title("Episode rewards")
# # compute and assign a rolling average of the data to provide a smoother graph
# reward_moving_average = (
#     np.convolve(
#         np.array(env.return_queue).flatten(), np.ones(rolling_length), mode="valid"
#     )
#     / rolling_length
# )
# axs.plot(range(len(reward_moving_average)), reward_moving_average)
# plt.tight_layout()
# plt.show()
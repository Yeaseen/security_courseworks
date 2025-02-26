from __future__ import annotations

from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import gymnasium as gym


env = gym.make('Blackjack-v1', natural=False, sab=False)

done = False
observation, info = env.reset()

action = env.action_space.sample()
observation, reward, terminated, truncated, info = env.step(action)


class BlackjackAgent:
    def __init__(
        self,
        env,
        learning_rate: float,
        initial_epsilon: float,
        epsilon_decay: float,
        final_epsilon: float,
        exploration: str = "epsilon_greedy",  # "boltzmann" or "epsilon_greedy"
        discount_factor: float = 0.95,
    ):
        self.q_values = defaultdict(lambda: np.zeros(env.action_space.n))
        self.lr = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon
        self.exploration = exploration
        self.training_error = []
    
    def boltzmann_policy(self, obs: tuple[int, int, bool]):
        q_values = self.q_values[obs]
        exp_q = np.exp(q_values / max(self.epsilon, 1e-3))  # Avoid divide by zero
        probabilities = exp_q / np.sum(exp_q)
        return np.random.choice(len(q_values), p=probabilities)

    def get_action(self, env, obs: tuple[int, int, bool]) -> int:
        if self.exploration == "epsilon_greedy":
            if np.random.random() < self.epsilon:
                return env.action_space.sample()
            return int(np.argmax(self.q_values[obs]))
        elif self.exploration == "boltzmann":
            return self.boltzmann_policy(obs)

    def update(
        self,
        obs: tuple[int, int, bool],
        action: int,
        reward: float,
        terminated: bool,
        next_obs: tuple[int, int, bool],
    ):
        future_q_value = (not terminated) * np.max(self.q_values[next_obs])
        temporal_difference = (
            reward + self.discount_factor * future_q_value - self.q_values[obs][action]
        )
        self.q_values[obs][action] += self.lr * temporal_difference
        self.training_error.append(temporal_difference)

    def decay_epsilon(self):
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)


# Hyperparameters
learning_rate = 0.01
n_episodes = 100_000
epsilon_values = [1.0, 0.5, 0.1]
epsilon_decay = 1.0 / (n_episodes / 2)
final_epsilon = 0.1

exploration_methods = ["epsilon_greedy", "boltzmann"]
results = {}

for method in exploration_methods:
    for epsilon in epsilon_values:
        agent = BlackjackAgent(
            env=env,
            learning_rate=learning_rate,
            initial_epsilon=epsilon,
            epsilon_decay=epsilon_decay,
            final_epsilon=final_epsilon,
            exploration=method,
        )

        env = gym.make('Blackjack-v1', natural=False, sab=False)  # Create a fresh environment
        env = gym.wrappers.RecordEpisodeStatistics(env, buffer_length=n_episodes)
        for episode in tqdm(range(n_episodes), desc=f"Q-Learning ({method}, ε={epsilon})"):
            obs, info = env.reset()
            done = False

            while not done:
                action = agent.get_action(env, obs)
                step_result = env.step(action)
                if '_stats_key' in step_result[4]:  # Check the info dictionary
                    del step_result[4]['_stats_key']
                next_obs, reward, terminated, truncated, info = step_result
                agent.update(obs, action, reward, terminated, next_obs)
                done = terminated or truncated
                obs = next_obs

            agent.decay_epsilon()
        
        results[(method, epsilon)] = np.array(env.return_queue)

# Plot results
fig, axs = plt.subplots(figsize=(12, 5))
axs.set_title("Q-Learning Performance Comparison")
axs.set_xlabel("Episode")
axs.set_ylabel("Average Reward")

for key, reward_data in results.items():
    method, epsilon = key
    rolling_length = 5000
    reward_moving_average = np.convolve(reward_data, np.ones(rolling_length) / rolling_length, mode='valid')
    axs.plot(reward_moving_average, label=f"{method} (ε={epsilon})")

axs.legend()
plt.tight_layout()
plt.savefig("q_learning_exploration_comparison.png")

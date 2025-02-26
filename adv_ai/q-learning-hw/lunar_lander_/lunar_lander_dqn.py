import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque
import matplotlib.pyplot as plt
from tqdm import tqdm

# Set up the LunarLander environment
env = gym.make("LunarLander-v3")

# Define the DQN Model
class DQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_dim, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, action_dim)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Define the DQN Agent
class DQNAgent:
    def __init__(self, state_dim, action_dim, lr=0.001, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01, buffer_size=10000, batch_size=64):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.batch_size = batch_size
        
        self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        
        self.q_network = DQN(state_dim, action_dim).to(self.device)
        self.target_network = DQN(state_dim, action_dim).to(self.device)
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.target_network.eval()
        
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        self.replay_buffer = deque(maxlen=buffer_size)
    
    def select_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.action_dim)
        state = torch.tensor(state, dtype=torch.float32).to(self.device).unsqueeze(0)
        with torch.no_grad():
            q_values = self.q_network(state)
        return torch.argmax(q_values).item()
    
    def store_transition(self, state, action, reward, next_state, done):
        self.replay_buffer.append((state, action, reward, next_state, done))
    
    def train(self):
        if len(self.replay_buffer) < self.batch_size:
            return
        batch = random.sample(self.replay_buffer, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        states = torch.tensor(states, dtype=torch.float32).to(self.device)
        actions = torch.tensor(actions, dtype=torch.int64).to(self.device)
        rewards = torch.tensor(rewards, dtype=torch.float32).to(self.device)
        next_states = torch.tensor(next_states, dtype=torch.float32).to(self.device)
        dones = torch.tensor(dones, dtype=torch.float32).to(self.device)
        
        q_values = self.q_network(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        next_q_values = self.target_network(next_states).max(1)[0]
        target_q_values = rewards + self.gamma * next_q_values * (1 - dones)
        
        loss = nn.MSELoss()(q_values, target_q_values.detach())
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
    
    def update_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    
    def update_target_network(self):
        self.target_network.load_state_dict(self.q_network.state_dict())

# Training Parameters
num_episodes = 1000
update_target_every = 10
reward_log = []

state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n
agent = DQNAgent(state_dim, action_dim)

# Training Loop
for episode in tqdm(range(num_episodes), desc="Training DQN"):
    state, _ = env.reset()
    total_reward = 0
    done = False
    
    while not done:
        action = agent.select_action(state)
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        
        agent.store_transition(state, action, reward, next_state, done)
        agent.train()
        state = next_state
        total_reward += reward
    
    reward_log.append(total_reward)
    agent.update_epsilon()
    
    if episode % update_target_every == 0:
        agent.update_target_network()

# Plot Learning Curve
rolling_length = 50
reward_moving_average = np.convolve(reward_log, np.ones(rolling_length) / rolling_length, mode='valid')
plt.figure(figsize=(12, 5))
plt.title("DQN- MSE with Hard Target Network Update")
plt.xlabel("Episode")
plt.ylabel("Average Reward")
plt.plot(reward_moving_average, label='DQN Moving Average Reward')
plt.legend()
plt.tight_layout()
plt.savefig("dqn_mse_soft_upgrade.png")

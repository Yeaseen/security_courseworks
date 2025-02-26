import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque
import matplotlib.pyplot as plt
from tqdm import tqdm

# Set up the CarRacing environment
env = gym.make("CarRacing-v3", domain_randomize=False, continuous=False)

# Define the CNN-based DQN Model
class CNN_DQN(nn.Module):
    def __init__(self, input_shape, action_dim):
        super(CNN_DQN, self).__init__()
        self.conv1 = nn.Conv2d(input_shape[0], 32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)

        # Compute the flattened size dynamically
        with torch.no_grad():
            dummy_input = torch.zeros(1, *input_shape)  # Create a dummy input tensor
            dummy_out = self._forward_conv(dummy_input)
            conv_out_size = dummy_out.view(1, -1).size(1)  # Flattened size

        self.fc1 = nn.Linear(conv_out_size, 512)
        self.fc2 = nn.Linear(512, action_dim)

    def _forward_conv(self, x):
        """Helper function to pass input through convolutional layers only"""
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        return x

    def forward(self, x):
        x = self._forward_conv(x)
        x = x.view(x.size(0), -1)  # Flatten dynamically
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

# Define the DQN Agent
class DQNAgent:
    def __init__(self, input_shape, action_dim, lr=0.00025, gamma=0.99, tau=0.005, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01, buffer_size=50000, batch_size=32):
        self.input_shape = input_shape
        self.action_dim = action_dim
        self.lr = lr
        self.gamma = gamma
        self.tau = tau  # Soft update parameter
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.batch_size = batch_size
        
        self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        
        self.q_network = CNN_DQN(input_shape, action_dim).to(self.device)
        self.target_network = CNN_DQN(input_shape, action_dim).to(self.device)
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.target_network.eval()
        
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        self.replay_buffer = deque(maxlen=buffer_size)
    
    def select_action(self, state):
        state = np.transpose(state, (2, 0, 1))  # Convert (H, W, C) -> (C, H, W)
        state = torch.tensor(state, dtype=torch.float32).to(self.device).unsqueeze(0) / 255.0  # Normalize
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.action_dim)
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

        # Convert (H, W, C) -> (C, H, W) and normalize
        states = np.array([np.transpose(s, (2, 0, 1)) for s in states]) / 255.0
        next_states = np.array([np.transpose(s, (2, 0, 1)) for s in next_states]) / 255.0

        states = torch.tensor(states, dtype=torch.float32).to(self.device)
        next_states = torch.tensor(next_states, dtype=torch.float32).to(self.device)

        actions = torch.tensor(actions, dtype=torch.int64).to(self.device)
        rewards = torch.tensor(rewards, dtype=torch.float32).to(self.device)
        dones = torch.tensor(dones, dtype=torch.float32).to(self.device)

        q_values = self.q_network(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        next_q_values = self.target_network(next_states).max(1)[0]
        target_q_values = rewards + self.gamma * next_q_values * (1 - dones)

        loss = nn.SmoothL1Loss()(q_values, target_q_values.detach())  # Huber Loss
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
    
    def update_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    
    def soft_update_target_network(self):
        for target_param, local_param in zip(self.target_network.parameters(), self.q_network.parameters()):
            target_param.data.copy_(self.tau * local_param.data + (1.0 - self.tau) * target_param.data)

# Training Parameters
num_episodes = 1000
update_target_every = 10
reward_log = []

input_shape = (3, 96, 96)  # RGB input, 96x96 resolution
action_dim = 5  # Discretized steering, acceleration, and braking
agent = DQNAgent(input_shape, action_dim)

# Training Loop
for episode in tqdm(range(num_episodes), desc="Training DQN - CarRacing"):
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
    agent.soft_update_target_network()

# Plot Learning Curve
rolling_length = 50
reward_moving_average = np.convolve(reward_log, np.ones(rolling_length) / rolling_length, mode='valid')
plt.figure(figsize=(12, 5))
plt.title("DQN Learning Curve - Car Racing")
plt.xlabel("Episode")
plt.ylabel("Average Reward")
plt.plot(reward_moving_average, label='DQN Moving Average Reward')
plt.legend()
plt.tight_layout()
plt.savefig("dqn_car_racing.png")

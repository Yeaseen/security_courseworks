import gym
import argparse
import pygame
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam
from teleop import collect_demos
from mountain_car_bc import collect_human_demos, torchify_demos, train_policy, PolicyNetwork, evaluate_policy

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def collect_random_interaction_data(num_iters):
    """Collect random interaction data from the environment"""
    state_next_state = []
    actions = []
    env = gym.make('MountainCar-v0')
    
    for _ in range(num_iters):
        obs = env.reset()
        done = False
        
        while not done:
            # Sample random action
            action = env.action_space.sample()
            next_obs, reward, done, info = env.step(action)
            
            # Store state transition and action
            state_next_state.append(np.concatenate((obs, next_obs)))
            actions.append(action)
            
            obs = next_obs
            
    env.close()
    return np.array(state_next_state), np.array(actions)

class InvDynamicsNetwork(nn.Module):
    """Neural network for inverse dynamics model"""
    def __init__(self, input_dim=4, hidden_dim=128):
        super().__init__()
        # Network architecture
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, 3)  # 3 discrete actions
        
        # Initialize weights
        self.apply(self._init_weights)
        
    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.xavier_uniform_(module.weight)
            if module.bias is not None:
                module.bias.data.zero_()

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def train_inverse_dynamics(inv_dyn, s_s2_torch, a_torch, num_epochs=100, batch_size=64):
    """Train the inverse dynamics model"""
    optimizer = Adam(inv_dyn.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    # Convert to dataset size
    dataset_size = s_s2_torch.shape[0]
    
    for epoch in range(num_epochs):
        total_loss = 0
        num_batches = 0
        
        # Create random permutation for batching
        indices = torch.randperm(dataset_size)
        
        # Train in batches
        for start_idx in range(0, dataset_size, batch_size):
            # Get batch indices
            batch_indices = indices[start_idx:start_idx + batch_size]
            
            # Get batch data
            state_batch = s_s2_torch[batch_indices]
            action_batch = a_torch[batch_indices]
            
            # Forward pass
            outputs = inv_dyn(state_batch)
            loss = criterion(outputs, action_batch)
            
            # Backward pass and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            num_batches += 1
        
        # Print progress
        if (epoch + 1) % 10 == 0:
            avg_loss = total_loss / num_batches
            print(f'Epoch [{epoch+1}/{num_epochs}], Average Loss: {avg_loss:.4f}')
    
    return inv_dyn

def evaluate_inverse_dynamics(inv_dyn, s_s2_test, a_test):
    """Evaluate the inverse dynamics model"""
    with torch.no_grad():
        outputs = inv_dyn(s_s2_test)
        _, predicted = torch.max(outputs.data, 1)
        total = a_test.size(0)
        correct = (predicted == a_test).sum().item()
        accuracy = 100 * correct / total
        print(f'Inverse Dynamics Test Accuracy: {accuracy:.2f}%')
    return accuracy

def main(args):
    # 1. Collect random interaction data
    print("Collecting random interaction data...")
    s_s2, acs = collect_random_interaction_data(args.num_interactions)
    s_s2_torch = torch.from_numpy(np.array(s_s2)).float().to(device)
    a_torch = torch.from_numpy(np.array(acs)).long().to(device)

    # 2. Initialize and train inverse dynamics model
    print("Training inverse dynamics model...")
    inv_dyn = InvDynamicsNetwork().to(device)
    inv_dyn = train_inverse_dynamics(inv_dyn, s_s2_torch, a_torch, 
                                   num_epochs=args.num_epochs)

    # 3. Evaluate inverse dynamics model
    print("Evaluating inverse dynamics model...")
    evaluate_inverse_dynamics(inv_dyn, s_s2_torch, a_torch)

    # 4. Collect human demonstrations
    print("Collecting human demonstrations...")
    demos = collect_human_demos(args.num_demos)

    # 5. Process demonstrations
    print("Processing demonstrations...")
    obs, acs_true, obs2 = torchify_demos(demos)

    # 6. Predict actions using inverse dynamics model
    print("Predicting actions from demonstrations...")
    state_trans = torch.cat((obs, obs2), dim=1)
    outputs = inv_dyn(state_trans)
    _, acs = torch.max(outputs, 1)

    # 7. Train policy using predicted actions
    print("Training policy using behavioral cloning...")
    pi = PolicyNetwork().to(device)
    train_policy(obs, acs, pi, args.num_bc_iters)

    # 8. Evaluate final policy
    print("Evaluating final policy...")
    evaluate_policy(pi, args.num_evals)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mountain Car BCO Implementation')
    parser.add_argument('--num_demos', default=1, type=int,
                        help='number of human demonstrations to collect')
    parser.add_argument('--num_bc_iters', default=100, type=int,
                        help='number of iterations to run BC')
    parser.add_argument('--num_evals', default=10, type=int,
                        help='number of times to evaluate policy')
    parser.add_argument('--num_interactions', default=100, type=int,
                        help='number of random interactions to collect')
    parser.add_argument('--num_epochs', default=100, type=int,
                        help='number of epochs to train inverse dynamics model')

    args = parser.parse_args()
    main(args)
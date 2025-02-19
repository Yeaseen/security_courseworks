import mdp
import mdp_utils

# Initialize the grid world environment using the basic setup
# To explore different MDP configurations, modify or replace 'gen_simple_world' with another function like 'gen_simple_world2'
grid_env = mdp.gen_simple_world3()

# Display the reward values assigned to each grid cell
print("Rewards in the grid:")
mdp_utils.print_array_as_grid(grid_env.rewards, grid_env)

# Generate and display a random policy which randomly assigns an action to each state
print("Visualizing a random policy:")
random_policy = mdp_utils.get_random_policy(grid_env)
mdp_utils.visualize_policy(random_policy, grid_env)

# Perform value iteration to find the optimal state values and the corresponding policy
print("--- Starting Value Iteration ---")
values_from_value_iteration = mdp_utils.value_iteration(grid_env)
print("State values after Value Iteration:")
mdp_utils.print_array_as_grid(values_from_value_iteration, grid_env)

# Extract and display the optimal policy derived from the value iteration results
optimal_policy_from_vi = mdp_utils.extract_optimal_policy(values_from_value_iteration, grid_env)
print("Optimal Policy from Value Iteration:")
mdp_utils.visualize_policy(optimal_policy_from_vi, grid_env)

# Perform policy iteration to find the optimal policy directly along with the state values
print("--- Starting Policy Iteration ---")
optimal_policy_from_pi, values_from_policy_iteration = mdp_utils.policy_iteration(grid_env)
print("Optimal Policy from Policy Iteration:")
mdp_utils.visualize_policy(optimal_policy_from_pi, grid_env)
print("State values from Policy Iteration:")
mdp_utils.print_array_as_grid(values_from_policy_iteration, grid_env)

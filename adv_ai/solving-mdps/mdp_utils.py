from mdp import MDP
import numpy as np


def get_random_policy(env):
    n = env.num_states
    a = env.num_actions
    policy =  np.random.randint(0, a, size=n) 
    return policy

def action_to_string(act, UP=0, DOWN=1, LEFT=2, RIGHT=3):
    if act == UP:
        return "^"
    elif act == DOWN:
        return "v"
    elif act == LEFT:
        return "<"
    elif act == RIGHT:
        return ">"
    else:
        return NotImplementedError




def visualize_policy(policy, env):
    """
  prints the policy of the MDP using text arrows and uses a '.' for terminals
  """
    count = 0
    for r in range(env.num_rows):
        policy_row = ""
        for c in range(env.num_cols):
            if count in env.terminals:
                policy_row += ".\t"    
            else:
                policy_row += action_to_string(policy[count]) + "\t"
            count += 1
        print(policy_row)


def print_array_as_grid(array_values, env):
    """
  Prints array as a grid
  :param array_values:
  :param env:
  :return:
  """
    count = 0
    for r in range(env.num_rows):
        print_row = ""
        for c in range(env.num_cols):
            print_row += "{:.2f}\t".format(array_values[count])
            count += 1
        print(print_row)




def value_iteration(env, epsilon=0.0001):
    """
    Run value iteration to find optimal values for each state
  :param env: the MDP
  :param epsilon: numerical precision for values to determine stopping condition
  :return: the vector of optimal values for each state in the MDP 
  """
    n = env.num_states
    V = np.zeros(n)
    
    while True:
        V_old = V.copy()
        delta = 0
        
        for s in range(n):
            if s in env.terminals:
                V[s] = env.rewards[s]
                continue
                
            # Find max value over all actions
            max_value = float('-inf')
            for a in range(env.num_actions):
                value = 0
                for next_s in range(n):
                    value += env.transitions[s][a][next_s] * \
                            (env.rewards[next_s] + env.gamma * V_old[next_s])
                max_value = max(max_value, value)
            V[s] = max_value
            delta = max(delta, abs(V[s] - V_old[s]))
            
        if delta < epsilon:
            break
            
    return V

def extract_optimal_policy(V, env):
    """ 
    Perform a one step lookahead to find optimal policy
    :param V: precomputed values from value iteration
    :param env: the MDP
    :return: the optimal policy
    """
    n = env.num_states
    optimal_policy = np.zeros(n, dtype=int)
    
    for s in range(n):
        if s in env.terminals:
            continue
            
        # Find action that maximizes value
        max_value = float('-inf')
        best_action = 0
        
        for a in range(env.num_actions):
            value = 0
            for next_s in range(n):
                value += env.transitions[s][a][next_s] * \
                        (env.rewards[next_s] + env.gamma * V[next_s])
            if value > max_value:
                max_value = value
                best_action = a
                
        optimal_policy[s] = best_action
        
    return optimal_policy

def policy_evaluation(policy, env, epsilon):
    """
    Evalute the policy and compute values in each state when executing the policy in the mdp
    :param policy: the policy to evaluate in the mdp
    :param env: markov decision process where we evaluate the policy
    :param epsilon: numerical precision desired
    :return: values of policy under mdp
    """
    n = env.num_states
    V = np.zeros(n)
    
    while True:
        delta = 0
        V_old = V.copy()
        
        for s in range(n):
            if s in env.terminals:
                V[s] = env.rewards[s]
                continue
                
            # Compute value for current policy
            a = policy[s]
            value = 0
            for next_s in range(n):
                value += env.transitions[s][a][next_s] * \
                        (env.rewards[next_s] + env.gamma * V_old[next_s])
            V[s] = value
            delta = max(delta, abs(V[s] - V_old[s]))
            
        if delta < epsilon:
            break
            
    return V

def policy_iteration(env, epsilon=0.0001):
    """
    Run policy iteration to find optimal values and policy
    :param env: markov decision process where we evaluate the policy
    :param epsilon: numerical precision desired
    :return: values of policy under mdp
    """
    n = env.num_states
    policy = get_random_policy(env)
    
    while True:
        # Policy evaluation
        V = policy_evaluation(policy, env, epsilon)
        
        # Policy improvement
        policy_stable = True
        for s in range(n):
            if s in env.terminals:
                continue
                
            old_action = policy[s]
            
            # Find best action
            max_value = float('-inf')
            best_action = 0
            
            for a in range(env.num_actions):
                value = 0
                for next_s in range(n):
                    value += env.transitions[s][a][next_s] * \
                            (env.rewards[next_s] + env.gamma * V[next_s])
                if value > max_value:
                    max_value = value
                    best_action = a
                    
            policy[s] = best_action
            
            if old_action != policy[s]:
                policy_stable = False
                
        if policy_stable:
            break
            
    return policy, V

import gymnasium as gym

env = gym.make("Blackjack-v1", render_mode="human")
obs, info = env.reset()
done = False

while not done:
    print(f"\nYour hand: {obs[0]}, Dealer shows: {obs[1]}, Usable Ace: {obs[2]}")
    action = input("Enter 'h' to hit or 's' to stand: ").strip().lower()
    
    if action == 'h':
        action = 1  # Hit
    elif action == 's':
        action = 0  # Stand
    else:
        print("Invalid input, please enter 'h' or 's'.")
        continue
    
    obs, reward, done, _, info = env.step(action)

# Print result
if reward == 1:
    print("\nYou won!")
elif reward == -1:
    print("\nYou lost!")
else:
    print("\nIt's a draw!")

env.close()

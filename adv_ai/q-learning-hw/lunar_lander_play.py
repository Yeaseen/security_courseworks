import gymnasium as gym
import argparse
import pygame


def simple_run(teleop=False):

    env = gym.make("LunarLander-v3", continuous=False, gravity=-10.0,
                   enable_wind=False, wind_power=15.0, turbulence_power=1.5, render_mode="human")
    obs, info = env.reset()

    done = False
    rewards = []
    while not done:
        # Control Branch for human teleop (Teleop=True, Heuristic=False)
        action = 0  # Default action = do nothing
        if teleop:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                action = 1  # Fire left orientation engine
            elif keys[pygame.K_UP]:
                action = 2  # Fire main engine
            elif keys[pygame.K_RIGHT]:
                action = 3  # Fire right orientation engine
            else:
                action = 0  # Default to doing nothing

        # Control Branch for Random Actions (Teleop=False, Heuristic=False)
        else:
            # Randomly Sample an Action
            action = env.action_space.sample()

        obs, rew, done, truncated, info = env.step(action)
        rewards.append(rew)
        env.render()

    print("Cumulative Reward:", sum(rewards))

if __name__ == "__main__":
    params = argparse.ArgumentParser()
    params.add_argument("--teleop", action="store_true", default=False, help="Use the keyboard keys to control the movement")
    #If you don't specify --teleop it will default to a random policy

    args = params.parse_args()

    simple_run(args.teleop)


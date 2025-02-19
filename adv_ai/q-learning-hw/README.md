# Homework 4: Q-learning

For this assignment you will be implementing a tabular Q-Learning agent to play Blackjack and also coding up a DQN agent to learn a policy for Lunar Lander. Write up a single report for your group and include all group member names when you submit to Canvas. Also include a zip file of your code.


## Part 0:

Set up a virtual environment using conda. 
```
conda create --name rl_env python=3.12
conda activate rl_env
```
### Gymnasium Installation
Then install gymnasium. On Linux and Mac, you should be able to run.
```
pip install swig gymnasium pygame Box2D
pip install "gymnasium[box2d,mujoco,toy_text]"
```

If you are developing on Windows, the above command should also work, but you may need to install Visual C++ 14.0 before you can install box2d. If you get an error, just follow the instructions in the error message if you get one. You should download Visual Studio Installer and then use it to get C++. Here are some useful instructions: https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst. 


Gymnasium is the most up-to-date and supported version of Gym that you played with for Homework 1. There are a few small differences between Gymnasium and Gym, but they follow the same overall structure and Gym is deprecated so it’s useful to get familiar with Gymnasium. Here is a link to documentation that you should skim to remind yourself how interactions with the environment works at a high-level: 
https://gymnasium.farama.org/introduction/basic_usage/ 

### PyTorch Installation
You will also need PyTorch installed. You don’t need to have a GPU since the problems we’ll be studying are simple, but if you have access to one you can install the GPU version and it might speed things up a bit; however, RL is often more CPU bound than GPU bound so you should be fine if you just want to install the CPU version (this is usually simpler). You can install PyTorch following the instructions here by selecting your OS and whether you want a GPU version or just CPU: 
https://pytorch.org/get-started/locally/ 


## Part 1: Tabular Q-Learning to Win Big at Blackjack!!

For part 1, we will be implementing a basic vanilla Q-Learning agent (no function approximation) to learn to win at the game of Blackjack. 
Before you start, read the description of the Blackjack environment on Gymnasium: https://gymnasium.farama.org/environments/toy_text/blackjack/ 
You can also find tutorials on how to play Blackjack online, but note that real-world Blackjack at has some extra rules and actions beyond what this environment allows. We assume all you can do is “hit” or “stick” (also called “stand”).
There are a couple versions. We will just use the default version corresponding to 
gym.make('Blackjack-v1', natural=False, sab=False)

You can play the game yourself by running the script included in this repo to get a better idea of the observation space. Giving the argument `render_mode="human"` will also display a simple visualization (note, you don't want to have human render mode when running Q-learning since it will just slow things down, but it's fun to play with and may be useful for debugging).
```
python blackjack_play.py
```


Your goal is to implement a Tabular Q-Learning agent that will interact with the environment to play Blackjack and will keep track of Q-values using a lookup table. 

Before starting, reread the section on Q-Learning from Sutton and Barto: 
http://incompleteideas.net/book/ebook/node65.html 

If you get stuck, this is also good reference, but your implementation doesn’t have to be this complicated: 
https://gymnasium.farama.org/tutorials/training_agents/blackjack_tutorial/#sphx-glr-tutorials-training-agents-blackjack-tutorial-py

To show that your agent is learning, plot a learning curve where time is the x-axis and cumulative reward over trajectories is the y-axis. You should see a noisy but roughly monotonically improving performance curve. If you want a smoother curve you can periodically pause updates and run your learned policy (remember the policy is implicit in the Q-values so just taking argmax over Q-values gives you the current policy) over several episodes and average the rewards and plot these averages over time. Compare the performance of Q-Learning to a purely random policy. Give a brief report on your results.

Note that this game, like most at a Casino, is hard to consistently win, so you shouldn't be surprised if your win rate isn't very high. But you should do much better than a random policy.


## Part 2: Landing on the Moon using DQN!
Next we will implement the DQN algorithm. 
https://github.com/dsbrown1331/advanced-ai/blob/main/readings/dqn.pdf 
You will be following along with this tutorial: 
https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html 
Note that this tutorial uses a slightly more sophisticated version of DQN that improves on the original Nature paper by using a Huber loss instead of MSE and using soft rather than hard target updates.

Also note the above tutorial focuses on training a policy for CartPole, but your goal is to train DQN learn how a policy for Lunar Lander instead. Feel free to start with CartPole since it is easier and should work out of the box using the code provided in the above tutorial. You should only require minimal changes to make the code work for Lunar Lander, but make sure you understand what is happening. If you're confused, Generative AI, is usually pretty good at explaining code snippets. Try it out and see.

Before you start coding things up take some time to familiarize yourself with the Lunar Lander environment. 
https://gymnasium.farama.org/environments/box2d/lunar_lander/ 
Then use the included human teleoperation code in this repo `lunar_lander_play.py` to try landing yourself, you use the left right and up arrows. You can also use this code to watch a random policy (just run the command without the --teleop argument).
```
 python .\lunar_lander_play.py --teleop
```

It's a little tricky to land smoothly. We will see if we can use RL to learn a policy that is better than you are. 

Provide evidence that your policy learns and improves overtime. You don’t have to spend a ton of time tuning hyper parameters or run policy learning for a really long time. Don't worry about getting a perfect policy. You should see significant improvement over a random policy after a few minutes of training. Report the performance of your learned policy versus a random policy. Add some code to visualize your policy using the env.render() functionality in Gymnasium. How does it do? Can it perform better than you can? Briefly report on your findings and answer the above questions.

## Extra Credit 1: 
Test both Boltzmann exploration and epsilon-greedy with several different epsilons for Q-Learning on Blackjack and report what you learn about how they perform.

## Extra Credit 2: 
Code up a DQN agent that uses convolutional layers as well as fully connected layers so you can learn from pixels and get an agent to learn how to drive in the Car Racing environment (one of the simplest pixel-based Gymnasium tasks) https://gymnasium.farama.org/environments/box2d/car_racing/. Note, having access to a GPU may be beneficial for speeding up the learning and it may take a while for the agent to learn. You don't have to fully solve the task, but you should be able to demonstrate that your agent is learning and that it learns to perform significantly better than a random policy.

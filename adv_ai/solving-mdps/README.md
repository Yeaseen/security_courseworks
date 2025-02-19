# solving-mdps
Homework on value and policy iteration.

Turn in one written report per group via Canvas with all group members names on the report. Also turn in your code.

This section of the Sutton and Barto RL book is a good supplement to go along with the class slides:
http://incompleteideas.net/book/ebook/node40.html
Note that they assume the most general form of a stochastic policy (outputs a probability distribution over actions given a state). In this homework we will only consider deterministic policies. We don't lose any optimality by doing this since for any MDP, there is always an optimal deterministic policy.

## Setup
Clone/Download this repository. Set up a virtual environment (conda, pyvenv) if you wish. Then install numpy. 
You can run `conda install numpy`, `pip install numpy`, `pip3 install numpy`. If you want you can just use the same conda env from homework 1 since this will already have numpy installed.

## Part 1: 
Finish `homework3.py` by filling in the relevant methods in `mdp_utils.py`. We've provided you with some gridworld starter code and a simple MDP class in `mdp.py`.
You will need to access the properties of the MDP class to solve the problems (i.e. you need to query the env’s transition probabilities, action space, rewards, etc). Read through the entire `mdp.py` file before you start working on `mdp_utils.py`. There are also some helper functions provided for you in `mdp_utils.py`.

When you finish, you should get the same results from both Value Iteration and Policy Iteration.

In your report include the output of `homework3.py`.

## Part 2:
You will now get to have fun and build intutioon by playing around with some different MDPs. You can start by making a copy of the method `gen_simple_world()` (e.g., make a `gen_simple_world2()` method) and make changes/tweaks from there. For example, maybe change the reward function, change the noise in the MDP, or change the terminal states. Does the change in the optimal policy make sense? Report and discuss two different MDPs you made by making tweaks to the MDP from Part 1 that resulted in a different optimal policy than you got in Part 1. 

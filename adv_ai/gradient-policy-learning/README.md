# Homework 5: Policy Gradients

For this homework you may work in groups of up to 3 students. Turn in one submission for your group with all your team members' names when submit to Canvas. Submit all source code along with a writeup that answers and discusses the questions and experiments below.

## Setup
You should use the rl_env conda environment that you set up for [Homework 4](https://github.com/dsbrown1331/q-learning-homework) This should have almost all the packages you need. The only thing missing that will need to add is scipy. To install this just activate your environment and call `conda install scipy`. You may also find [MatplotLib useful](https://matplotlib.org/stable/tutorials/index.html) for plotting results and can install this via `pip install matplotlib`. 

## Part 1a: Understanding and Implementing a Basic Policy Gradient Algorithm
If you haven't already, read through [Part 1](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html) and [Part 2](https://spinningup.openai.com/en/latest/spinningup/rl_intro2.html) of the Policy Gradient Tutorial on SpinningUp.

Now start [Part 3](https://spinningup.openai.com/en/latest/spinningup/rl_intro3.html)
This tutorial will walk you through the most basic policy gradient implementation. Follow along with the tutorial and stop before the "Expected Grad-Log-Prob Lemma" section.
Now take a look at `.\1_simple_pg_gymnasium.py` in this gitrepo (this is just an updated version of what is in the SpinningUp tutorial adapted to use gymnasium rather than the deprecated gym).
Make sure that everyone on your team understands each line: play around with the code, add some print lines, run through using a debugger, copy and paste code into your favorite AI program to have it explain parts that are confusing, etc. 
You can run the code by calling 
`
python 1_simple_pg_gymnasium.py
`
This will run a simple policy gradient algorithm on the CartPole environment, a classic RL control benchmark. Read up on CartPole [here](https://gymnasium.farama.org/environments/classic_control/cart_pole/.)

You won't see anything except printouts showing learning over time. By default it will run for 50 epochs. Feel free to play around with and change any of the hyperparameters and code. **Report on what you see and what it means. Is the agent learning? What happens to it's performance over time? Is it monotonically improving? Discuss why you think that is.**

## Part 1b: Understanding and Implementing a Basic Policy Gradient Algorithm

It's kind of boring to not see learning happening. Edit the code so that after each epoch you visually render a rollout from the current policy so you can watch the agent over time. You should add new code that renders 1 episode after each call to train_one_epoch. Make a second version of the env with render_mode=“human” and step through an episode so you can see what’s happening. When referencing your policy, call `get_action` using `with torch.no_grad():` so that forward passes at test time are not updating the network gradient. What do you notice qualitatively about how its policy changes over time? Include one screenshot of your rendered policy in your report to show that your visualization is working.

## Part 2: Reducing Variance with Reward-to-Go

Continue reading the tutorial from [here](https://spinningup.openai.com/en/latest/spinningup/rl_intro3.html#expected-grad-log-prob-lemma)
and read through the section "Implementing Reward-to-Go Policy Gradient". 
Make a copy of your simple policy gradient code and make the recommended changes to your code so that you implement the reward-to-go version. Make sure you understand what is going on.

Run your new code and compare the performance with your older version. Run each method 3-5 times (make sure you add code to save the data that is currently just being printed to the screen) and include a plot of the two methods' learning curve (average return vs. timesteps). Briefly discuss what your experiment shows. Do you notice any differences? Is one approach better? Why or why not?

## Part 3: Continuous Actions
Let's first make our code more general purpose. You probably noticed that your simple policy gradient code only works with discrete actions. One of the benefits of policy gradient methods is that they work for both discrete and continuous action spaces. Take a look through the `core.py` file that is included in this gitrepo. This contains code that you can use to make your policy gradient code work automatically for either continuous or discrete envs in Gymnasium. Note if you want to use it on an image-based domain it will require more work, but it should work for any environment with a lower-dimensional state space represented by a vector which is fine for our purposes.

You should use the `MLPActorCritic` class in `core.py` to make your policy gradient code work automatically for either continuous or discrete envs in Gymnasium. Note you won't need to worry about the `discount_cumsum` method, just focus on using the MLP actor classes in your code. We won't be using the value function prediction from the critic yet but we will in the next section. For now you can just leave it as a random network and ignore the v output when calling step. If you don't plan to do the extra credit you can just use the `MLPActor` class.

You should now be able to run both continuous and discrete action domains. Test your code on CartPole to make sure it still works on a discrete action environment. Next pick a continuous action environment from Gymnasium to test your code. You can look at some of the [MuJoCo locomotion tasks](https://gymnasium.farama.org/environments/mujoco/). InvertedPendulum is also pretty simple and is our recommendation as the simplest task to test on. Hopper is a bit more complex but more interesting and you should see learning happen but it will take longer. Some of the others are quite complex so I wouldn't recommend trying them without a good CPU and GPU and a better codebase than what we've been playing around with.

Report on what environment you chose and the results of using your code. You may want to play around with hyperparameters a bit to see what works best. Report what you tried and learned.

## Extra Credit A: Baselines and Generalized Advantage Estimation
Read the rest of the tutorial starting with the section on "Baselines in Policy Gradients".

Now we want to actually learn a value function to use as part of a baseline. Rather than using the reward to go, we will be implementing generalized advantage estimation and using our estimate of the advantage function as the weight in the policy gradient update. We will be approximating the value function using a neural network. The good news for you is that this is already setup if you are using the `MLPActorCritic` class. If you're not using that class go back and follow the instructions for Part 3. 

We've got a neural network but we need to train it. As mentioned in the tutorial we've been following, the simplest way to train a value function is via a standard MSE loss. Let's add that to our code. You will now have two PyTorch optimizers, one for the policy and one for the value function. You will still collect a batch of on-policy data. Same as before you'll update the policy using a policy gradient, but now you will use the generalized advantage estimation to estimate the advantage function like we talked about in class. You can read more about it [here](https://danieltakeshi.github.io/2017/04/02/notes-on-the-generalized-advantage-estimation-paper/). You will also update the value function using each batch of data via a standard MSE loss. You will be simply pushing the predicted value of each state with the true cumulative return experienced in the batch (the reward-to-go from that state). Note that to improve stability, you may want to perform several gradient steps of value learning for each step of policy update.

After working on this for a while, if you're really stuck, take a look here at this implementation of vanilla policy gradient + GAE that also uses `core.py`: https://github.com/openai/spinningup/blob/master/spinup/algos/pytorch/vpg/vpg.py
Also this [documentation](https://spinningup.openai.com/en/latest/algorithms/vpg.html) may help understand the code better.
Note this code uses some parallelization using mpi, but you don't have to parallelize your code unless you really want to. This implementation also recommends normalizing the advantage estimates after computing them (lines 79-81) and this is probably a good thing to try in your implementation as well.

Test out your implementation on CartPole and a continuous action environment of your choice. Report and discuss how your policy performs. How do your results compare to performance without a baseline?


## Extra Credit B:

Go through the PPO [documentation](https://spinningup.openai.com/en/latest/algorithms/ppo.html) and [implementation](https://github.com/openai/spinningup/tree/master/spinup/algos/pytorch/ppo) and read through the code. Remember, AI (e.g. ChatGPT, CoPilot) can be your friend here and help you understand complex lines of code. We encourage you to explore using generative AI by uploading the code and asking questions about it. See what happens and if you find it useful and accurate. Include in your report a discussion about what is different in this implementation of PPO compared to your simple policy gradient code. What is the same. What things did you learn while going through the code? What parts are still confusing or unclear? Note, you don't have to get this code to run, but you're welcome to try (it will require using OpenMPI (https://spinningup.openai.com/en/latest/user/installation.html) or stripping out that code and will likely be non-trivial if you're not on Ubuntu).

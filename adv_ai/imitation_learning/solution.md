# MountainCar-v0 Experiment Analysis

## Part 1: Initial Observations and Challenges

We notice that the car(`MountainCar-v0`) oscillates back and forth in a valley, trying to reach the flag at the top of the right hill. The code uses random actions (`env.action_space.sample()`), explaining the back-and-forth movement without apparent progress. The car rarely (if ever) reaches the goal, as random actions are not effective for such a goal-directed task.

### Challenges:

MountainCar is challenging for reinforcement learning (RL) for several key reasons:

- **Sparse Rewards:** The agent only receives a positive reward when it reaches the goal (flag) at the top of the hill. During all other times, it receives a small negative reward (-1 per timestep in the standard implementation). This creates a `sparse reward` problem where the agent gets no immediate helpful feedback, be it positive or negative, about whether its actions are helping it make progress toward the goal. Without sufficient exploration, the agent cannot find the sequence of actions required to escape the valley.

- **Local Optima Problem:** In the MountainCar environment, a naive trial-and-error approach often gets stuck in a local optimum, where the agent learns to stay near the valley bottom to minimize short-term penalties (-1 per step) instead of building momentum to reach the goal. Building momentum requires temporarily moving away from the goal, which increases immediate penalties, but a random or greedy strategy fails to recognize this as necessary for long-term success. Without intermediate rewards or effective exploration strategies, the agent cannot escape the valley, leading to stagnation and suboptimal performance.

<p align="center">
  <img src="images/1.png" alt="observation" width="300" height="200">
</p>

## Part 2: Effective Strategy

We found the strategy of alternating left and right movements up the hill (left, right, left, right) to be most effective, achieving a best score of -140.

<p align="center">
  <img src="images/2.png" alt="strategy" width="300" height="200">
</p>

## Part 3: Imitation Learning Performance

The agent often gets stuck and consistently scores -200, indicating poor imitation of the demonstrated strategy.

### Experiment Parameters:

- **Learning Rates:** 1e-2, 1e-3
- **Number of Iterations:** 100, 150, 200
- **Hidden Sizes:** 64, 128

## Part 4: Behavioral Cloning (BC) Improvements

With 5 demonstrations, the BC model actually escapes the valley, suggesting that with more demonstrations, the model can access a larger variety of state-action pairs, enhancing learning.

Wow! With the number of demos 5, the BC works better and does ACTUALLY escape the valley! This is quite interesting at this point.

### Effective Parameters:

- **Learning Rate:** 1e-3
- **Number of Iterations:** 100
- **Hidden Sizes:** 128

Here, we are providing two runs:

<div style="display: flex; justify-content: center;">
  <img src="images/4.png" alt="Description of image 3" width="300" height="200" style="margin-right: 20px;">
  <img src="images/3.png" alt="Description of image 4" width="300" height="200">
</div>

We think the following factors might help the BC model.

- With more demonstrations, the model has access to a larger variety of state-action pairs, enabling it to learn a more robust mapping from states to optimal actions.
- The neural network has enough capacity (128 hidden units) to learn the complex relationship between states and actions in the MountainCar environment without being excessively large, which could lead to overfitting. The learning_rate and number_iterations were standard here.

→ Does the agent copy the strategy you used?
Yes. The agent copied the strategy we demonstrated in the human demo part. We provided the strategy in all 5 demos: Left, Right, Left, Right!
Here, we have one thought on the BC’s performance: all 5 demos had the same pattern which might have helped the BC model to imitate the human demo strategy.

## Part 5: Mixed Demonstration Quality

The policy is learning to mimic the average behavior across both demonstrations - that's why we see faster oscillations (combining the bad demo's behavior with the good demo's behavior) even though it's not achieving good performance. Bad demonstrations are problematic because behavioral cloning treats all demonstration data equally - it doesn't distinguish between "good" and "bad" behaviors. It tries to find a policy to explain all the observed state-action pairs, essentially averaging across them. This leads to compromised behavior that may capture surface features (like oscillation frequency) without learning the strategic elements (like building up momentum in the right way) needed for success.

One potential solution would be to weight demonstrations based on their "quality" during training. This would make the policy learn more strongly from successful demonstrations while reducing the influence of poor ones.

## Part 6: BC Model Limitations

The BC model failed to imitate the strategy from 5 human demonstrations effectively, possibly due to inadequate reward scenarios in the demonstrations.

## Part 7: Behavioral Cloning from Observation (BCO)

### Key Changes for BCO Implementation:

1. Create a pre-demonstration phase for random state transition collection.
2. Build a dataset of (st, at, st+1) tuples.
3. Train an inverse dynamics model to predict actions from state transitions.
4. Infer missing actions using the trained inverse model.

## Part 8: Inverse Dynamics Model Integration

Initially, the BC model's performance dropped significantly with the inclusion of the inverse dynamics model. We kept the same parameters for the neural network of the inverse dynamics model.

Later, we changed the number of interactions from 10 to 100 and the number of demos from 5 to 12, then it performed well, but only once. We couldn’t reproduce the same kind of result with the same setup. The other results were worse. We think it was once successful because of the bias of the inverse dynamics model’s training dataset.

<p align="center">
  <img src="images/5.png" alt="inverse_dynamics_model" width="300" height="200">
</p>

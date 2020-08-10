import gym
import gym_pid
from DDPG import Agent
import numpy as np
import utils

env = gym.make('pid-v0')
agent = Agent(alpha=0.000025, beta=0.00025, input_dims=[2], tau=0.001, env=env,
              batch_size=64,  layer1_size=400, layer2_size=300, n_actions=2)

#agent.load_models()
np.random.seed(0)

score_history=[]
for i in range(200):
    obs = env.reset()
    done = False
    score = 0
    while not done:
        act = agent.choose_action(obs)
        new_state, reward, done, info = env.step(act)
        agent.remember(obs, act, reward, new_state, int(done))
        agent.learn()
        score += reward
        obs = new_state
        #env.render()
    score_history.append(score)

    if i % 25 == 0:
        agent.save_models()

    print('episode ', i, 'score %.2f' % score,
          'trailing 25 games avg %.3f' % np.mean(score_history[-25:]))

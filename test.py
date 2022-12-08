import gym

env = gym.make("RubiksCube-v1")
env.reset(seed=0,options={'scramble': True})
env.render()

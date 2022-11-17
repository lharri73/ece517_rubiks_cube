from rubiks.env.cube import RubiksCubeEnv
from rubiks.consts import *
import gym

env = gym.make("RubiksCube-v1")
env.reset(seed=0,options={'scramble': True})
env.render()

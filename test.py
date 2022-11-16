from rubiks.env.cube import RubiksCubeEnv
from rubiks.consts import *
import gym

env = gym.make("RubiksCube-v1")
env.reset(options={'scramble': False})
env.render()
env.rotate_cc(0)
env.rotate_cc(0)
env.rotate_cc(0)
env.render()
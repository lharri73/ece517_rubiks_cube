from gym.envs.registration import register
import warnings

register(
    id='RubiksCube-v1',
    entry_point='rubiks.env.cube:RubiksCubeEnv',
)

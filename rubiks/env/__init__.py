from gym.envs.registration import register

register(
    id='RubiksCube-v0',
    entry_point='rubiks_cube.cube:RubiksCubeEnv',
)

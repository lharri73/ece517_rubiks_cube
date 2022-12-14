import gym
# noinspection PyUnresolvedReferences
from rubiks.env.cube import RubiksCubeEnv
from rubiks.lib.yoinked.fridrich import Fridrich



def main():
    env = gym.make('RubiksCube-v1')
    state, _ = env.reset(options={"scramble": True})
    print(env.get_string_state())

    solver = Fridrich()
    solver.init_scramble(env)
    solver.solve()

    moves = solver.get_moves()
    print(''.join(moves))



if __name__ == "__main__":
    main()

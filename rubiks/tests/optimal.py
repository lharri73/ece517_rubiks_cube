import gym
from rubiks.env.cube import RubiksCubeEnv
from rubiks.lib.yoinked.two_phase import TwoPhaseSolver
import time


def main():
    env = gym.make("RubiksCube-v1")
    state, _ = env.reset(seed=2, options={'scramble': True})
    env.rotate_cube_about_right()
    env.render()
    print(env.get_string_state())
    env.rotate_cube_about_left()

    solver = TwoPhaseSolver()
    solver.init_scramble(env)
    tic = time.time()
    solver.solve()
    toc = time.time()
    print("Solved in {} seconds".format(toc - tic))

    moves = solver.get_moves()
    print(''.join(moves))


if __name__ == "__main__":
    main()

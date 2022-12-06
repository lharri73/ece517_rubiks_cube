from rubiks.env.cube import RubiksCubeEnv
from sys import stdin
import gym
from matplotlib import pyplot as plt
from utils import move

if __name__ == "__main__":
    env = gym.make("RubiksCube")
    state, _ = env.reset(seed=0, options={'scramble': True})
    # move('r.ub', env.step)

    first = True
    while True:
        env.render(show=False)
        plt.show(block=False)
        if first:
            plt.pause(1)
            first = False
        plt.pause(0.1)

        print("input: ", end='')
        input_ = stdin.readline().strip()
        if input_ == '':
            break
        elif input_ == "reset":
            state, _ = env.reset(seed=0, options={'scramble': True})
        elif input_ == "exit" or input_ == "quit":
            break
        elif input_ == "rot":
            env.rotate_cube()
        else:
            move(input_, env.step)

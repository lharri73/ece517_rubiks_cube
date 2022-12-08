from rubiks.env.cube import RubiksCubeEnv
from sys import stdin
import gym
from matplotlib import pyplot as plt
from utils import move

def init():
    env = gym.make("RubiksCube-v1")
    state, _ = env.reset(seed=2, options={'scramble': False})
    # move('.u.u', env.step)
    return env

def main():
    env = init()
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
            env = init()
        elif input_ == "exit" or input_ == "quit":
            break
        elif input_ == "rot":
            env.rotate_cube()
        elif input_ == "solve":
            env.reset(options={"scramble": False})
        elif input_.startswith("scramble"):
            options = input_.split()
            if len(options) != 2:
                print("usage: scramble <seed>")
            else:
                env.reset(seed=int(options[1]))
        else:
            try:
                move(input_, env.step)
            except KeyError:
                print(f"Unknown command: '{input_}'")


if __name__ == "__main__":
    main()

    # fdf.duu.f.luulfuu.l.ul.ul.u.lu.b.ubuuffuu.f.uf.u.fru.r.u.fufru.r.u.fru.rur.u.ruruurbbrf.rbbr.frullfflb.lffl.blrruuruurruurruuruurr
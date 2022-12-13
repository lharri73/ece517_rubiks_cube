# noinspection PyUnresolvedReferences
from rubiks.env.cube import RubiksCubeEnv
from sys import stdin
import gym
from matplotlib import pyplot as plt
from rubiks.lib.utils.cube_utils import move

def reset():
    env = gym.make("RubiksCube-v1")
    state, _ = env.reset(seed=2, options={'scramble': False})
    # move('.u.u', env.step)
    return env

def main():
    env = reset()
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
        if input_ == "reset":
            env = reset()
        elif input_ == "exit" or input_ == "quit":
            break
        elif input_ == "rot":
            env.rotate_cube_clock()
        elif input_ == "solve":
            env.reset(options={"scramble": False})
        elif input_.startswith("scramble"):
            options = input_.split()
            if len(options) != 2:
                print("usage: scramble <seed>")
            else:
                env.reset(seed=int(options[1]))
        elif input_.startswith("init"):
            options = input_.split()
            if len(options) != 2:
                print("usage: init <string_state>")
            else:
                env.reset(options={"fromState": options[1]})
        elif input_ == "ss":
            print(env.get_string_state())
        elif input_.startswith("help"):
            print("reset:               destroy the old environment and create a new one")
            print("exit:                quit interactive_cobe")
            print("rot:                 rotate the cube 90 degrees clockwise")
            print("solve:               reset the cube to a solved state")
            print("scramble <seed>:     reset the cube to a random state with the given seed")
            print("init <string_state>: reset the cube to the given state")
            print("<move_sequence>:     apply the given move sequence to the cube")
            print("help:                print this message")
        else:
            try:
                move(input_, env.step)
            except KeyError:
                print(f"Unknown command: '{input_}'\nTry help")


if __name__ == "__main__":
    main()

    # fdf.duu.f.luulfuu.l.ul.ul.u.lu.b.ubuuffuu.f.uf.u.fru.r.u.fufru.r.u.fru.rur.u.ruruurbbrf.rbbr.frullfflb.lffl.blrruuruurruurruuruurr

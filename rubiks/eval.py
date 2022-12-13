from rubiks.lib.utils.args import parse_args
from rubiks.lib.utils.model_utils import load_model
from rubiks.lib.astar.impl import CubeSearch

import gym
# noinspection PyUnresolvedReferences
from rubiks.env.cube import RubiksCubeEnv
import torch







def main():
    args = parse_args()
    model = load_model(args)
    model.eval()

    env = gym.make('RubiksCube-v1')
    state, _ = env.reset(options={"scramble": True, "min": 13, "max": 15, "print_scramble": True})
    env.render()

    solver = CubeSearch(model, env)
    path = solver.get_actions()
    print(path)

    # done = False
    # while not done:
    #     action = get_next_action_model(model, env)
    #     print(action)
    #     state, _, done, _, _ = env.step(actionDict[action])
    #     env.render()


if __name__ == "__main__":
    main()
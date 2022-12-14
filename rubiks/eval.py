from rubiks.lib.utils.args import parse_args
from rubiks.lib.utils.model_utils import load_model, get_next_action_model
from rubiks.lib.utils.timeout import timeout
from rubiks.lib.astar.impl import CubeSearch
from rubiks.lib.consts import actionDict
from matplotlib import pyplot as plt

import gym
# noinspection PyUnresolvedReferences
from rubiks.env.cube import RubiksCubeEnv
import torch
from tqdm import trange, tqdm
import numpy as np
import pickle

class ModelCounter:
    def __init__(self, model):
        self.model = model
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.model(*args, **kwargs)

def main():
    args = parse_args()
    model = load_model(args)
    model.eval()
    counter = ModelCounter(model)

    env = gym.make('RubiksCube-v1')
    num_samples = 50
    counts = np.empty((10,num_samples, 2))

    # for i in trange(1, 10,position=0, desc="Scramble len"):
    #     for j in trange(num_samples,position=1,desc="Iteration"):
    #         state, _ = env.reset(options={"scramble": True, "min": i, "max": i, "print_scramble": False, "applySeed": False})
    #
    #         solver = CubeSearch(counter, env)
    #         try:
    #             path = solver.get_actions()
    #         except AssertionError:
    #             tqdm.write("failed to find solution with a star")
    #             counter.count = 0
    #         counts[i,j, 0] = counter.count
    #
    #         counter.count = 0
    #         try:
    #             with timeout(5):
    #                 done = False
    #                 while not done:
    #                     action = get_next_action_model(counter, env)
    #                     state, _, done, _, _ = env.step(actionDict[action])
    #         except:
    #             tqdm.write(f"timeout on get_next_action with scramble length {i}")
    #             counter.count = 0
    #         counts[i,j, 1] = counter.count

    # pickle.dump(counts, open("counts.p", "wb"))
    with open("counts.p", "rb") as f:
        counts = pickle.load(f)



    means = np.empty((10, 2))
    for i in range(10):
        maska = np.logical_and(counts[i,:,0]!=0, counts[i,:,0] < 2**12)
        maskb = np.logical_and(counts[i,:,1]!=0, counts[i,:,1] < 2**12)
        means[i,0] = np.mean(counts[i, maska, 0])
        means[i,1] = np.mean(counts[i,maskb, 1])

    plt.plot(means[:,0], label="A*")
    plt.plot(means[:,1], label="Greedy")
    plt.xlabel("Scramble length")
    plt.ylabel("Number of model calls")
    plt.legend()
    plt.savefig("tests/images/performancetest.pdf")

    # with open("counts.p", "rb") as f:
    #     counts = pickle.load(f)



if __name__ == "__main__":
    main()
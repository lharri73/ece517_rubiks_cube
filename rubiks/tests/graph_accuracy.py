from matplotlib import pyplot as plt
from rubiks.lib.utils.model_utils import load_model
from rubiks.lib.utils.args import parse_args
from tqdm import trange
from rubiks.lib.utils.model_utils import calc_cost_to_go
import pickle

# noinspection PyUnresolvedReferences
from rubiks.env.cube import RubiksCubeEnv
import gym
import random
import numpy as np
import torch


def main():
    args = parse_args()
    model = load_model(args)
    model.eval()
    env = gym.make('RubiksCube-v1')
    random.seed(None)

    num_samples = 1000

    results = np.empty((25))
    solves = np.empty((25*num_samples))

    # for i in trange(25,position=2, desc="Scramble len"):
    #     for j in trange(num_samples,position=0,desc="Iteration"):
    #         state, _ = env.reset(options={"scramble": True, "min": i, "max": i, "applySeed": False})
    #         correct = calc_cost_to_go(env)
    #         mine = model(torch.from_numpy(state).float().flatten()).cpu().detach().numpy()
    #         diff = abs(correct - mine)
    #         results[i] = (j * results[i] + diff) / (j + 1)
    #         solves[i*num_samples+j] = correct
    #
    # obj = {
    #     "results": results,
    #     "solves": solves
    # }
    # pickle.dump(obj, open("results.p", "wb"))

    with open("results.p", "rb") as f:
        obj = pickle.load(f)
        results = obj["results"]
        solves = obj["solves"]

    # solves = solves.reshape((25, num_samples))
    # print(solves)

    fig, ax = plt.subplots(3,1, figsize=(6,6))

    ax[0].plot(results, label="Error")
    ax[0].set_xlabel("Scramble Length")
    ax[0].set_ylabel("Error")
    ax[0].set_title("Model Error vs Scramble Length")
    # print(solves)

    # counts, bins = np.histogram(solves.astype(np.int32), bins=range(26), density=True)
    ax[1].hist(solves, bins=range(26),density=True, color="red")
    ax[1].set_ylabel("Ratio of samples")
    ax[1].set_xlabel("Solve Length")

    solves = solves.reshape((25, num_samples))
    solves = np.mean(solves, axis=1)

    ax[2].plot(solves, label="Optimal Solve Length", color="green")
    ax[2].set_xlabel("Scramble Length")
    ax[2].set_ylabel("Optimal Solve Length")

    plt.subplots_adjust(hspace=0.5)
    # plt.show()
    plt.savefig('images/accuracy.pdf')

if __name__ == "__main__":
    main()
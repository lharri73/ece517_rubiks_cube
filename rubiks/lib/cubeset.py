import torch
from torch.utils.data import IterableDataset
import gym
from torch.utils.data.dataset import T_co

# noinspection PyUnresolvedReferences
from rubiks.env.cube import RubiksCubeEnv
from rubiks.lib.ctg import calc_cost_to_go
import warnings
import os
import random


class CubeDataset(IterableDataset):
    def __init__(self, length):
        warnings.simplefilter('ignore')
        self.env = gym.make("RubiksCube-v1")
        warnings.resetwarnings()
        self.length = length
        self.origSeed = None


    def __len__(self):
        return self.length

    def __iter__(self):
        worker_info = torch.utils.data.get_worker_info()
        while True:
            state, _ = self.env.reset(seed=worker_info.seed, options={'scramble': True, 'min': 0, 'max': 25, 'applySeed': self.origSeed != worker_info.seed})
            self.origSeed = worker_info.seed

            ctg = calc_cost_to_go(self.env)
            yield torch.tensor(state.flatten(), dtype=torch.float), torch.tensor(ctg, dtype=torch.float)


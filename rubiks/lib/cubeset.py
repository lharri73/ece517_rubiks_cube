import torch
from torch.utils.data import IterableDataset
import gym
from torch.utils.data.dataset import T_co

# noinspection PyUnresolvedReferences
from rubiks.env.cube import RubiksCubeEnv
from rubiks.lib.ctg import calc_cost_to_go


class CubeDataset(IterableDataset):
    def __init__(self):
        self.env = gym.make("RubiksCube-v1")

    def __iter__(self):
        worker_info = torch.utils.data.get_worker_info()
        while True:
            state, _ = self.env.reset(seed=worker_info.seed, options={'scramble': True, 'min': 0, 'max': 25})

            ctg = calc_cost_to_go(self.env)
            yield state.flatten(), ctg


from rubiks.lib.astar.algo import AStar
# noinspection PyUnresolvedReferences
from rubiks.env.cube import RubiksCubeEnv
import numpy as np
from rubiks.lib.consts import actionDict, actionList, actionDictInv
from rubiks.lib.utils.model_utils import get_next_action_ctg
import gym
import torch

class CubeSearch(AStar):
    def __init__(self, model, env):
        self.model = model
        self.env = gym.make("RubiksCube-v1")
        self.states_trans = {}
        self.states_reverse = {}
        self.state_counter = 0
        self.states = np.full((0, len(actionList)), -1, dtype=np.int32)

        # states_mat is a matrix whose entries point to the index of the
        # state resulting from applying the action(column) at that index(row)
        # -1 indicates that the state is not visited
        # self.states_mat = np.full((2, len(actionDict)), -1)

        self._add_state(env.get_string_state())
        # goal state \/
        self._add_state("000000000444444444222222222333333333555555555111111111")

    def _add_state(self, state, origin=None):
        if state in self.states_reverse:
            return self.states_reverse[state]

        self.states_reverse[state] = self.state_counter
        self.states_trans[self.state_counter] = state
        if origin is not None:
            self.states[origin[0], origin[1]] = self.state_counter
        self.states = np.append(self.states, np.full((1, len(actionList)), -1, dtype=np.int32), axis=0)

        self.state_counter += 1
        assert self.state_counter < 2**12, "Searching too many states"
        return self.state_counter - 1

    def _restore_state(self, n1):
        state = self.states_trans[n1]
        npstate, _ = self.env.reset(options={"scramble": False, "fromState": state})
        torch_state = torch.tensor(npstate).flatten()
        return torch_state

    def heuristic_cost_estimate(self, n1, n2):
        """computes the cost to go to solve the cube. This doesn't depend on the goal since it's always the same"""

        npstate = self._restore_state(n1)

        ctg = self.model(npstate).cpu().detach().numpy()
        return ctg

    def distance_between(self, n1, n2):
        """this method always returns 1, as two 'neighbors' are always adajcent"""
        return 1

    def neighbors(self, node):
        """ For any node, return all possible resulting states.
        """
        self._restore_state(node)
        neighbors = []
        for action in actionList:
            with self.env.inverse_protect(action):
                state = self.env.get_string_state()
                neighbors.append(self._add_state(state, origin=(node, actionDict[action])))

        return neighbors

    def get_actions(self):
        path = self.astar(0,1)
        actions = []
        for i in range(len(path)-1):
            cur = path[i]
            next = path[i+1]
            if next == 1: break
            action = np.argwhere(self.states[cur] == next)
            actions.append(actionDictInv[action[0][0]])
        self._restore_state(cur)
        final = get_next_action_ctg(self.env)
        actions.append(final)

        return "".join(actions)
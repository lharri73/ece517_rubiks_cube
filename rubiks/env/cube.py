import random
from contextlib import contextmanager
from typing import Tuple

import gym
import numpy as np
from gym.core import ActType, ObsType
from matplotlib import pyplot as plt, colors

from rubiks.lib.consts import *
from rubiks.utils import rotate_state, rotate_state_rev, vis_state


class RubiksCubeEnv(gym.Env):
    cmap = {WHITE: 'white', RED: 'red', ORANGE: 'orange', YELLOW: 'yellow', GREEN: 'green', BLUE: 'blue'}
    actionList = ['f', 'r', 'l', 'u', 'd', 'b', '.f', '.r', '.l', '.u', '.d', '.b']
    actionDict = {'f': 0,  # orange
        'r': 1,  # green
        'l': 2,  # blue
        'u': 3,  # white
        'd': 4,  # yellow
        'b': 5,  # red
        '.f': 6, '.r': 7, '.l': 8, '.u': 9, '.d': 10, '.b': 11}

    def __init__(self, render_mode=None):
        self.state = np.empty((3, 3, 6), dtype=np.uint8)
        for i in range(6):
            self.state[:, :, i] = i
        self.observation_space = gym.spaces.Box(np.zeros((3, 3, 6)), np.full((3, 3, 6), 5), dtype=np.uint8)
        self.action_space = gym.spaces.Discrete(12)
        self.step_count = 0
        self.actions_taken = []

    def reset(self, seed=None, options=None):
        """
        Reset and randomize the cube

        :param seed: Seed for random number generator
        :param options: dictionary:
            {
                min: min number of steps to take for the scramble,
                max: max number of steps to take for the scramble,
                scramble: whether to scramble the cube
            }
        :return: state, {}
        """
        if options is None:
            options = {'min': 5, 'max': 20, 'scramble': True, "fromList": None, 'print_scramble': False}

        random.seed(seed)

        for i in range(6):
            self.state[:, :, i] = i

        if options.get("fromList", None) is not None:
            self._initialize_from_statelist(options.get("fromList", None))

        if options.get('scramble', False) and options.get("fromList", None) is None:
            self._scramble(random.randint(options.get('min', 5), options.get('max', 20)),
                           options.get('print_scramble', False))

        self.actions_taken = []
        self.step_count = 0

        return self.state, {}

    def _scramble(self, steps, print_scramble=False):

        for _ in range(steps):
            action = random.randint(0, 11)
            if print_scramble:
                print(self.actionList[action])
            self._action(action)

    def _action(self, action):
        self.actions_taken.append(action)

        if action == 0:
            self.rotate_clockwise(ORANGE)
        elif action == 1:
            self.rotate_clockwise(GREEN)
        elif action == 2:
            self.rotate_clockwise(BLUE)
        elif action == 3:
            self.rotate_clockwise(WHITE)
        elif action == 4:
            self.rotate_clockwise(YELLOW)
        elif action == 5:
            self.rotate_clockwise(RED)
        elif action == 6:
            self.rotate_cc(ORANGE)
        elif action == 7:
            self.rotate_cc(GREEN)
        elif action == 8:
            self.rotate_cc(BLUE)
        elif action == 9:
            self.rotate_cc(WHITE)
        elif action == 10:
            self.rotate_cc(YELLOW)
        elif action == 11:
            self.rotate_cc(RED)
        elif action == -1:
            self.rotate_cube_clock()
        elif action == -2:
            self.rotate_cube_cc()
        else:
            raise ValueError("Action must be on the interval [0,11]")

    def render(self, mode='human', show=True):
        vis_state(self.state)
        if show == True:
            plt.show()
        else:
            return

    def rotate_cc(self, side):
        self.state[:, :, side] = np.rot90(self.state[:, :, side])
        state = np.copy(self.state)

        if side == WHITE:
            self.state[0, :, ORANGE] = state[:, 2, BLUE]
            self.state[:, 2, BLUE] = np.flip(state[2, :, RED])
            self.state[2, :, RED] = state[:, 0, GREEN]
            self.state[:, 0, GREEN] = np.flip(state[0, :, ORANGE])
        elif side == RED:
            self.state[0, :, WHITE] = state[0, :, BLUE]
            self.state[0, :, GREEN] = state[0, :, WHITE]
            self.state[0, :, YELLOW] = state[0, :, GREEN]
            self.state[0, :, BLUE] = state[0, :, YELLOW]
        elif side == ORANGE:
            self.state[2, :, WHITE] = state[2, :, GREEN]
            self.state[2, :, GREEN] = state[2, :, YELLOW]
            self.state[2, :, YELLOW] = state[2, :, BLUE]
            self.state[2, :, BLUE] = state[2, :, WHITE]
        elif side == YELLOW:
            self.state[:, 2, GREEN] = state[0, :, RED]
            self.state[2, :, ORANGE] = np.flip(state[:, 2, GREEN])
            self.state[:, 0, BLUE] = state[2, :, ORANGE]
            self.state[0, :, RED] = np.flip(state[:, 0, BLUE])
        elif side == GREEN:
            self.state[:, 2, RED] = np.flip(state[:, 0, YELLOW])
            self.state[:, 2, WHITE] = state[:, 2, RED]
            self.state[:, 2, ORANGE] = state[:, 2, WHITE]
            self.state[:, 0, YELLOW] = np.flip(state[:, 2, ORANGE])
        elif side == BLUE:
            self.state[:, 0, RED] = state[:, 0, WHITE]
            self.state[:, 0, WHITE] = state[:, 0, ORANGE]
            self.state[:, 0, ORANGE] = np.flip(state[:, 2, YELLOW])
            self.state[:, 2, YELLOW] = np.flip(state[:, 0, RED])

        self.state = np.array(self.state)

    def rotate_clockwise(self, side):
        self.rotate_cc(side)
        self.rotate_cc(side)
        self.rotate_cc(side)

    def step(self, action: ActType) -> Tuple[ObsType, float, bool, bool, dict]:
        self._action(action)
        self.step_count += 1
        reward = -1

        done = True
        for i in range(6):
            if not np.all(self.state[:, :, i] == i):
                done = False
                break

        if done:
            reward = 100

        return self.state, reward, done, False, {}

    def rotate_cube_clock(self):
        self.state = rotate_state(self.state)
        self.actions_taken.append(-1)

    def rotate_cube_cc(self):
        self.state = rotate_state_rev(self.state)
        self.actions_taken.append(-2)

    @contextmanager
    def rotate_cube_context(self, k=1):
        """
        Positive k values rotate clockwise, negative values rotate counter-clockwise
        :param k:
        :return:
        """
        assert -4 < k < 4, "can only rotate 1-3 times"

        if k == 0:
            yield
            return
        elif k > 0:
            for i in range(k):
                self.rotate_cube_clock()
            yield

            for i in range(k):
                self.rotate_cube_cc()
        else:
            for i in range(-k):
                self.rotate_cube_cc()
            yield

            for i in range(-k):
                self.rotate_cube_clock()

    def _initialize_from_statelist(self, action_list):
        for action in action_list:
            if action == -1:
                self.rotate_cube_clock()
            elif action == -2:
                self.rotate_cube_cc()
            else:
                self._action(action)

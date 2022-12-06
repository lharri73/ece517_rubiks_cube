from typing import Tuple

from gym.core import ActType, ObsType
from matplotlib import pyplot as plt, colors
import numpy as np
import random

import gym
from rubiks.consts import *

class RubiksCubeEnv(gym.Env):

    cmap = {
        WHITE: 'white',
        RED: 'red',
        ORANGE: 'orange',
        YELLOW: 'yellow',
        GREEN: 'green',
        BLUE: 'blue'
    }
    actionList = [
        'f', 'r', 'l', 'u', 'd', 'b',
        '.f', '.r', '.l', '.u', '.d', '.b']
    actionDict = {
            'f':  0, # orange
            'r':  1, # green
            'l':  2, # blue
            'u':  3, # white
            'd':  4, # yellow
            'b':  5, # red
            '.f': 6,
            '.r': 7,
            '.l': 8,
            '.u': 9,
            '.d': 10,
            '.b': 11
        }
    def __init__(self, render_mode=None):
        self.state = np.empty((3,3,6), dtype=np.uint8)
        for i in range(6):
            self.state[:,:,i] = i
        self.observation_space = gym.spaces.Box(np.zeros((3,3,6)), np.full((3,3,6), 5),dtype=np.uint8)
        self.action_space = gym.spaces.Discrete(12)
        self.step_count = 0


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
            options = {'min': 5, 'max': 20, 'scramble': True}

        random.seed(seed)

        for i in range(6):
            self.state[:,:,i] = i

        self.step_count = 0
        if options.get('scramble', False):
            self._scramble(random.randint(options.get('min', 5), options.get('max', 20)))

        return self.state, {}

    def _scramble(self, steps):
        for _ in range(steps):
            action = random.randint(0, 11)
            self._action(action)


    def _action(self, action):
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
        else:
            raise ValueError("Action must be on the interval [0,11]")

    def render(self, mode='human', show=True):
        image = np.full((9,12), 6)
        image[3:6,0:3] = self.state[:,:,BLUE]        ## Blue side
        image[3:6,3:6] = self.state[:,:,WHITE]       ## White side
        image[3:6,6:9] = self.state[:,:,GREEN]       ## Green Side
        image[3:6,9:12] = self.state[:,:,YELLOW]     ## Yellow side
        image[0:3,3:6] = self.state[:,:,RED]         ## red side
        image[6:9,3:6] = self.state[:,:,ORANGE]      ## orange side

        colorList = list(self.cmap.values()) + ["black"]
        cmape = colors.ListedColormap(colorList)
        plt.imshow(image, cmap=cmape)
        plt.text(4,4,'U', fontsize='x-large', horizontalalignment='center', fontweight='bold', verticalalignment='center')
        plt.text(1, 4, 'L', fontsize='x-large', horizontalalignment='center', fontweight='bold',
                 verticalalignment='center')
        plt.text(4, 1, 'B', fontsize='x-large', horizontalalignment='center', fontweight='bold',
                 verticalalignment='center')
        plt.text(7, 4, 'R', fontsize='x-large', horizontalalignment='center', fontweight='bold',
                 verticalalignment='center')
        plt.text(10, 4, 'D', fontsize='x-large', horizontalalignment='center', fontweight='bold',
                 verticalalignment='center')
        plt.text(4, 7, 'F', fontsize='x-large', horizontalalignment='center', fontweight='bold',
                 verticalalignment='center')
        plt.axis('off')
        if show == True:
            plt.show()
        else:
            return


    def rotate_cc(self, side):
        self.state[:,:,side] = np.rot90(self.state[:,:,side])
        state = np.copy(self.state)

        if side == WHITE:
            self.state[0,:,ORANGE] = state[:,2,BLUE]
            self.state[:,2,BLUE] = np.flip(state[2,:,RED])
            self.state[2,:,RED] = state[:,0,GREEN]
            self.state[:,0,GREEN] = np.flip(state[0,:,ORANGE])
        elif side == RED:
            self.state[0,:,WHITE] = state[0,:,BLUE]
            self.state[0,:,GREEN] = state[0,:,WHITE]
            self.state[0,:,YELLOW] = state[0,:,GREEN]
            self.state[0,:,BLUE] = state[0,:,YELLOW]
        elif side == ORANGE:
            self.state[2,:,WHITE] = state[2,:,GREEN]
            self.state[2,:,GREEN] = state[2,:,YELLOW]
            self.state[2,:,YELLOW] = state[2,:,BLUE]
            self.state[2,:,BLUE] = state[2,:,WHITE]
        elif side == YELLOW:
            self.state[:,2,GREEN] = state[0,:,RED]
            self.state[2,:,ORANGE] = np.flip(state[:,2,GREEN])
            self.state[:,0,BLUE] = state[2,:,ORANGE]
            self.state[0,:,RED] = np.flip(state[:,0,BLUE])
        elif side == GREEN:
            self.state[:,2,RED] = np.flip(state[:,0,YELLOW])
            self.state[:,2,WHITE] = state[:,2,RED]
            self.state[:,2,ORANGE] = state[:,2,WHITE]
            self.state[:,0,YELLOW] = np.flip(state[:,2,ORANGE])
        elif side == BLUE:
            self.state[:,0,RED] = state[:,0,WHITE]
            self.state[:,0,WHITE] = state[:,0,ORANGE]
            self.state[:,0,ORANGE] = np.flip(state[:,2,YELLOW])
            self.state[:,2,YELLOW] = np.flip(state[:,0,RED])

        self.state = np.array(self.state)


    def rotate_clockwise(self, side):
        self.rotate_cc(side)
        self.rotate_cc(side)
        self.rotate_cc(side)


    def step(self, action: ActType) -> Tuple[ObsType, float, bool, bool, dict]:
        self._action(action)

        reward = -1

        done = True
        for i in range(6):
            if not np.all(self.state[:,:,i] == i):
                done = False
                break

        if done:
            reward = 100

        return self.state, reward, done, False, {}

    def rotate_cube(self):
        self.state[:,:,WHITE] = np.rot90(self.state[:,:,WHITE], k=3)
        tmp = np.copy(self.state[:,:,RED])
        self.state[:,:,RED] = np.rot90(self.state[:,:,BLUE],k=3)
        self.state[:,:,BLUE] = np.rot90(self.state[:,:,ORANGE],k=3)
        self.state[:,:,ORANGE] = np.rot90(self.state[:,:,GREEN],k=3)
        self.state[:,:,GREEN] = np.rot90(tmp, k=3)
        self.state[:,:,YELLOW] = np.rot90(self.state[:,:,YELLOW],k=1)


        self.state = np.array(self.state)

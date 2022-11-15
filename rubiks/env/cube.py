from matplotlib import pyplot as plt, colors
import numpy as np
import random

import gym

class RubiksCubeEnv(gym.Env):
    cmap = {
        0: 'white',
        1: 'red',
        2: 'orange',
        3: 'yellow',
        4: 'green',
        5: 'blue'
    }
    def __init__(self, render_mode=None):
        self.state = np.empty((3,3,6), dtype=np.uint8)
        for i in range(6):
            self.state[:,:,i] = i
        self.observation_space = gym.spaces.Box(np.zeros((3,3,6)), np.full((3,3,6), 5),dtype=np.uint8)
        self.action_space = gym.spaces.Discrete(12)
        self.step_count = 0


    def reset(self,seed=None, options=None):
        random.seed(seed)

        for i in range(6):
            self.state[:,:,i] = i

        self.step_count = 0 

    def render(self, mode='human'):
        image = np.full((9,12), 6)
        image[3:6,0:3] = self.state[:,:,5]      ## Blue side
        image[3:6,3:6] = self.state[:,:,0]      ## White side
        image[3:6,6:9] = self.state[:,:,4]      ## Green Side
        image[3:6,9:12] = self.state[:,:,3]     ## Yellow side
        image[0:3,3:6] = self.state[:,:,1]      ## red side
        image[6:9,3:6] = self.state[:,:,2]      ## orange side

        colorList = list(self.cmap.values()) + ["black"]
        cmape = colors.ListedColormap(colorList)
        plt.imshow(image, cmap=cmape)
        plt.show()


    def rotate_cc(self, side):
        self.state[:,:,side] = np.rot90(self.state[:,:,side])

        if side == 0:
            tmpg = np.copy(self.state[:,0,4])
            tmpo = np.copy(self.state[0,:,2])
            tmpb = np.copy(self.state[:,2,5])
            tmpr = np.copy(self.state[2,:,1])
            self.state[0,:,2] = tmpb
            self.state[:,2,5] = np.flip(tmpr)
            self.state[2,:,1] = tmpg
            self.state[:,0,4] = np.flip(tmpo)
        elif side == 1:
            state = np.copy(self.state)
            self.state[0,:,0] = state[0,:,5]
            self.state[0,:,4] = state[0,:,0]
            self.state[0,:,3] = state[0,:,4]
            self.state[0,:,5] = state[0,:,3]
        elif side == 2:
            state = np.copy(self.state)
            self.state[2,:,0] = state[2,:,4]
            self.state[2,:,4] = state[2,:,3]
            self.state[2,:,3] = state[2,:,5]
            self.state[2,:,5] = state[2,:,0]
        elif side == 3:
            state = np.copy(self.state)
            self.state[:,2,4] = state[0,:,1]
            self.state[2,:,2] = np.flip(state[:,2,4])
            self.state[:,0,5] = state[2,:,2]
            self.state[0,:,1] = np.flip(state[:,0,5])
        elif side == 4:
            state = np.copy(self.state)
            self.state[:,2,1] = state[0,:,3]
            self.state[:,2,0] = state[:,2,1]
            self.state[:,2,2] = state[:,2,0]
            self.state[:,0,3] = np.flip(state[:,2,2])
        elif side == 5:
            state = np.copy(self.state)
            self.state[:,0,1] = state[:,0,0]
            self.state[:,0,0] = state[:,0,2]
            self.state[:,0,2] = np.flip(state[:,2,3])
            self.state[:,2,3] = state[:,0,1]


    def rotate_clockwise(self, side):
        self.rotate_cc(side)
        self.rotate_cc(side)
        self.rotate_cc(side)

import functools
import operator

import gym.spaces
from rubiks.env.cube import RubiksCubeEnv
import time
import random
from rubiks.consts import *

class FridrichSolver:
    def __init__(self):
        self.env = gym.make("RubiksCube")
        self.state = None
        self.r = 0
        self.done = False

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

    def scramble(self):
        actions = [4]
        for action in actions:
            self.take_action(action)

    def take_action(self, action):
        self.last_action = action
        self.state, self.r, self.done, _, _ = self.env.step(action)

    def white_cross_solved(self):
        ## blue side
        blue_solved = self.state[1,2,BLUE] == BLUE and self.state[1,0,WHITE] == WHITE

        ## red side
        red_solved = self.state[2,2,RED] == RED and self.state[0,2,WHITE] == WHITE

        ## green solved
        green_solved = self.state[1,0,GREEN] == GREEN and self.state[1,2,WHITE] == WHITE

        ## orange solved
        orange_solved = self.state[0,1,ORANGE] == ORANGE and self.state[2,1,WHITE] == WHITE

        return blue_solved and red_solved and green_solved and orange_solved


    def get_matching_side(self,side, direction):
        if side == WHITE:
            if direction == UP:
                return RED
            elif direction == LEFT:
                return BLUE
            elif direction == RIGHT:
                return GREEN
            elif direction == DOWN:
                return ORANGE
        elif side == RED:
            if direction == UP:
                return YELLOW
            elif direction == DOWN:
                return WHITE
            elif direction == LEFT:
                return BLUE
            elif direction == RIGHT:
                return GREEN
        elif side == YELLOW:
            if direction == UP:
                return RED
            elif direction == LEFT:
                return GREEN
            elif direction == RIGHT:
                return BLUE
            elif direction == DOWN:
                return ORANGE
        elif side == GREEN:
            if direction == UP:
                return RED
            elif direction == LEFT:
                return WHITE
            elif direction == RIGHT:
                return YELLOW
            elif direction == DOWN:
                return ORANGE
        elif side == BLUE:
            if direction == UP:
                return RED
            elif direction == LEFT:
                return YELLOW
            elif direction == RIGHT:
                return WHITE
            elif direction == DOWN:
                return ORANGE
        elif side == ORANGE:
            if direction == UP:
                return WHITE
            elif direction == LEFT:
                return BLUE
            elif direction == RIGHT:
                return GREEN
            elif direction == DOWN:
                return YELLOW
        else:
            raise ValueError("Invalid side!")



    def solve_white_cross(self, target=GREEN):
        for row, col in [(0,1), (1,2), (2,1), (1,0)]:
            pass

    def solve(self):
        self.state, _ = self.env.reset(seed=0, options={'scramble': False})
        self.scramble()
        self.env.render()

        print(self.white_cross_solved())
        self.solve_white_cross()



        # done = False
        # while not done:
        #     action = random.randint(0, 11)
        #     print(f'action: {self.env.actionList[action]}')
        #     self.env.step(action)
        #     self.env.render()
        #     input()


if __name__ == "__main__":
    solver = FridrichSolver()
    solver.solve()

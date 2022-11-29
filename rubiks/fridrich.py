import functools
import operator

import gym.spaces
from rubiks.env.cube import RubiksCubeEnv
import time
import random
from rubiks.consts import *
from rubiks.utils import get_color, get_matching_idx

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


    def find_middle_piece(self, target1=GREEN, target2=WHITE):
        breaker = False
        for row, col, dir in [(0,1,UP), (1,2,RIGHT), (2,1,DOWN), (1,0,LEFT)]:
            for side in [WHITE, RED, ORANGE, YELLOW, GREEN, BLUE]:
                if self.state[row,col,side] == target1:
                    (facing_r, facing_c, facing_s, _), _ = get_matching_idx((row,col,side))
                    if self.state[facing_r,facing_c,facing_s] == target2:
                        breaker = True
                        break
            if breaker: break

        return row,col,side

    def white_cross_s1(self, target=GREEN):
        row, col, side = self.find_middle_piece(WHITE, target)
        if side == WHITE:
            if row == 1 and col == 2:
                ## do nothing, the white green piece is in the right place
                pass
            elif row == 0 and col == 1:
                passdd
        elif side == RED:
            pass
        elif side == ORANGE:
            pass
        elif side == YELLOW:
            pass
        elif side == GREEN:
            pass
        elif side == BLUE:
            pass
        else:
            raise ValueError("cannot find piece during white cross solve")

    def solve_white_cross(self):
        self.white_cross_s1(GREEN)



    def solve(self):
        self.state, _ = self.env.reset(seed=1, options={'scramble': True})
        # self.scramble()
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

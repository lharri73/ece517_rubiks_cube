import gym
import gym.spaces
import random
from rubiks.lib.consts import *
from rubiks.lib.utils.cube_utils import get_color, get_matching_idx, move
import numpy as np

class FridrichSolver:
    def __init__(self):
        self.env = gym.make("RubiksCube-v1")
        self.state = None
        self.r = 0
        self.done = False
        raise DeprecationWarning("Don't use this..doesn't work. Used the yoinked version")

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

    def move(self, actions):
        print(actions)
        move(actions, self.take_action)

    def white_cross_solved(self):
        ## blue side
        blue_solved = self.state[1,2,BLUE] == BLUE and self.state[1,0,WHITE] == WHITE

        ## red side
        red_solved = self.state[2,1,RED] == RED and self.state[0,1,WHITE] == WHITE

        ## green solved
        green_solved = self.state[1,0,GREEN] == GREEN and self.state[1,2,WHITE] == WHITE

        ## orange solved
        orange_solved = self.state[0,1,ORANGE] == ORANGE and self.state[2,1,WHITE] == WHITE

        return blue_solved and red_solved and green_solved and orange_solved


    def find_middle_piece(self, target1=GREEN, target2=WHITE):
        """
        side will be the side that target1 is on
        """
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

    def rotate_idx_90(self, *idx):
        mat = np.zeros((3,3))
        mat[idx] = 1
        mat = np.rot90(mat)
        new_idx_flat = np.argmax(mat)
        new_idx = np.unravel_index(new_idx_flat, (3,3))
        return new_idx


    def white_cross_s1(self, target=GREEN):
        row, col, side = self.find_middle_piece(WHITE, target)
        # self.rotate_idx_90(0,0)
        print(f"found white/green on {get_color(side)}")
        if side == WHITE:
            if row == 0 and col == 1:
                self.move(".b.ubu")
            elif row == 1 and col == 0:
                self.move('luu.luu')
            elif row == 1 and col == 2:
                ## in the right place
                pass
            elif row == 2 and col == 1:
                self.move('fu.f.u')
                pass
        elif side == RED:
            if row == 1 and col == 0:
                self.move('uuluu')
            elif row == 0 and col ==1:
                self.move('.ubu.r')
            elif row == 1 and col == 2:
                self.move('.r')
            elif row == 2 and col == 1:
                self.move('.b.r')
        elif side == ORANGE:
            if row == 0  and col == 1:
                self.move('fr')
            elif row == 1 and col == 0:
                self.move('uu.luu')
            elif row == 1 and col == 2:
                self.move('r')
            elif row == 2 and col == 1:
                self.move('u.f.ur')
        elif side == YELLOW:
            if row == 0 and col == 1:
                self.move('.drr')
            elif row == 1 and col == 0:
                self.move('rr')
            elif row == 1 and col == 2:
                self.move('ddrr')
            elif row == 2 and col == 1:
                self.move('drr')
            pass
        elif side == GREEN:
            if row == 0 and col == 1:
                self.move(".ubu")
            elif row == 1 and col == 0:
                self.move('r.ubu')
            elif row == 1 and col == 2:
                self.move('.r.ubu')
            elif row == 2 and col == 1:
                self.move('u.f.u')
        elif side == BLUE:
            if row == 0 and col == 1:
                self.move('.u.bu')
            elif row == 1 and col == 0:
                self.move('d.frf')
            elif row == 1 and col == 2:
                self.move('luf.u')
            elif row ==2 and col == 1:
                self.move('uf.u')
        else:
            raise ValueError("cannot find piece during white cross solve")

    def solve_white_cross(self):
        self.white_cross_s1(GREEN)
        self.env.rotate_cube()
        self.white_cross_s1(RED)
        self.env.rotate_cube()
        self.white_cross_s1(BLUE)
        self.env.rotate_cube()
        self.white_cross_s1(ORANGE)
        self.env.rotate_cube()



    def solve(self, seed=None, render=True):
        if seed is None:
            seed = random.randint(0,int(1e99))

        print(seed)
        self.state, _ = self.env.reset(seed=seed, options={"scramble": False})
        self.move('.r.ful')
        # self.scramble()

        if render:
            self.env.render()

        # print(self.white_cross_solved())
        self.solve_white_cross()
        if render:
            self.env.render()


        # done = False
        # while not done:
        #     action = random.randint(0, 11)
        #     print(f'action: {self.env.actionList[action]}')
        #     self.env.step(action)
        #     self.env.render()
        #     input()


def solve_many():
    solver = FridrichSolver()
    for i in range(100000):
        print(f'i = {i:6d}, seed = ', end='')
        solver.solve(seed=None,render=False)
        assert solver.white_cross_solved()

def solve_once():
    solver = FridrichSolver();
    solver.solve(seed=0,render=True)

if __name__ == "__main__":
    solve_once()



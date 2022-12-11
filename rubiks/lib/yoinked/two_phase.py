from rubiks.lib.solver import Solver
from rubiks.lib.consts import *
# noinspection PyUnresolvedReferences
from rubiks.env.cube import RubiksCubeEnv
from twophase import solver as sv
import gym
import numpy as np

class TwoPhaseSolver(Solver):
    env_state_translation = {
        WHITE: "U",
        GREEN: "R",
        ORANGE: "F",
        YELLOW: "D",
        BLUE: "L",
        RED: "B"
    }

    move_translation = {
        "U1": 'u',
        "U2": 'uu',
        "U3": '.u',
        "R1": 'r',
        "R2": 'rr',
        "R3": '.r',
        "F1": 'f',
        "F2": 'ff',
        "F3": '.f',
        "D1": 'd',
        "D2": 'dd',
        "D3": '.d',
        "L1": 'l',
        "L2": 'll',
        "L3": '.l',
        "B1": 'b',
        "B2": 'bb',
        "B3": '.b',
        "(0f)": '',
    }

    def __init__(self):
        super().__init__()
        self.moves = None
        self.intermediate_states = None
        self.state = None
        self.solved = False

    def init_scramble(self, env):
        cube_str = ""
        for side in [WHITE, GREEN, ORANGE, YELLOW, BLUE, RED]:
            cur_slice = env.state[:,:,side]
            if side in [YELLOW, RED]:
                cur_slice = np.fliplr(np.flipud(cur_slice))
            elif side == GREEN:
                cur_slice = np.rot90(cur_slice,k=3)
            elif side == BLUE:
                cur_slice = np.rot90(cur_slice,k=1)
            for row in range(3):
                for col in range(3):
                    cube_str += self.env_state_translation[cur_slice[row,col]]
        self.state = cube_str

    def solve(self):
        moves = sv.solve(self.state)
        self.moves = moves.split(' ')
        self.solved = True

    def get_moves(self):
        for move in self.moves:
            if move.startswith('('):
                continue
            try:
                cur_move = self.move_translation[move]
            except KeyError as e:
                raise Exception(f"Invalid move: {move}\n\tMove string: '{' '.join(self.moves)}'")
            yield cur_move

    def get_intermediate_states(self):
        assert self.solved, "Cube must be solved before getting intermediate states"

        env: "RubiksCubeEnv" = gym.make('RubiksCube-v1')
        env.reset(options={"fromState": self.initial_scramble})
        states = []
        move_str = "".join(self.get_moves())
        for action in move_str:
            state, _, _, _, _ = action
            states.append(state)

        return states

import gym.spaces
from rubiks.env.cube import RubiksCubeEnv
import time
import random

class FridrichSolver:
    def __init__(self):
        self.env = gym.make("RubiksCube")

    def solve(self):
        self.env.reset()
        self.env.render(seed=0)

        done = False
        while not done:
            action = random.randint(0, 11)
            print(f'action: {self.env.actionList[action]}')
            self.env.step(action)
            self.env.render()
            input()


if __name__ == "__main__":
    solver = FridrichSolver()
    solver.solve()

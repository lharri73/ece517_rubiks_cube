import gym.spaces
from rubiks.env.cube import RubiksCubeEnv
import time
import random

class FridrichSolver:
    def __init__(self, random=True):
        self.env = gym.make("RubiksCube-v0")
        if random:
            self.seed = int(time.time())
        else:
            self.seed = 0

    def solve(self):
        self.env.reset()
        self.env.render()

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

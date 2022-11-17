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

    def scramble(self):
        self.env.reset(seed=self.seed, options={'min': 5, 'max': 10})
        self.env.render()

        done = False
        while not done:
            action = random.randint(0, 11)
            print(f'action: {self.actionList[action]}')
            self.env.step(action)
            self.env.render()
            input()


if __name__ == "__main__":
    solver = FridrichSolver()
    solver.scramble()

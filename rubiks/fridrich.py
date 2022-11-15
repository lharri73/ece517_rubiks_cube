import gym.spaces
import gym_Rubiks_Cube
import time
import random

class FridrichSolver:
    actionDict = {
            'f':  0,
            'r':  1,
            'l':  2,
            'u':  3,
            'd':  4,
            'b':  5,
            '.f': 6,
            '.r': 7,
            '.l': 8,
            '.u': 9,
            '.d': 10,
            '.b': 11
        }
    actionList = [
        'f', 'r', 'l', 'u', 'd', 'b',
        '.f', '.r', '.l', '.u', '.d', '.b']
    def __init__(self, random=True):
        self.env = gym.make("RubiksCube-v0")
        if random:
            self.seed = int(time.time())
        else:
            self.seed = 0

    def scramble(self):
        self.env.setScramble(5, 10, True)
        self.env.reset(seed=self.seed)
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

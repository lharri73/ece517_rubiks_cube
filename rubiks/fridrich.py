import gym.spaces
import gym_Rubiks_Cube
import time

class FridrichSolver:
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



if __name__ == "__main__":
    solver = FridrichSolver()
    solver.scramble()

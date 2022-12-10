from abc import ABC, abstractmethod


class Solver(ABC):
    def __init__(self):
        self.state = None
        self.solved = False

    @abstractmethod
    def init_scramble(self, env):
        """
        translate the state of our cube to the state of this solver
        :param state:
        :return:
        """
        raise NotImplemented()

    @abstractmethod
    def solve(self):
        pass

    @abstractmethod
    def get_moves(self):
        pass

    @abstractmethod
    def get_intermediate_states(self):
        pass

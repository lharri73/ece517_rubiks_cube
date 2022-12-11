from rubiks.lib.yoinked.two_phase import TwoPhaseSolver
from rubiks.lib.yoinked.fridrich import Fridrich


def calc_cost_to_go(env):
    """
    Calculate the cost to go for the current state
    :param env:
    :return:
    """
    solver = TwoPhaseSolver()
    solver.init_scramble(env)
    solver.solve()
    two_phase_moves = len(list(solver.get_moves()))

    solver = Fridrich()
    solver.init_scramble(env)
    solver.solve()
    fridrich_moves = len(list(solver.get_moves()))
    return min(two_phase_moves, fridrich_moves)


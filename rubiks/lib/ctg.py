from rubiks.lib.yoinked.two_phase import TwoPhaseSolver
from rubiks.lib.yoinked.fridrich import Fridrich
from rubiks.lib.utils.model_utils import timeout


def calc_cost_to_go(env):
    """
    Calculate the cost to go for the current state
    :param env:
    :return:
    """
    try:
        with timeout(4):
            solver = TwoPhaseSolver()
            solver.init_scramble(env)
            solver.solve()
            two_phase_moves = len(list(solver.get_moves()))
    except TimeoutError:
        print("twophase timeout")
        two_phase_moves = 2048


    try:
        with timeout(3):
            solver = Fridrich()
            solver.init_scramble(env)
            solver.solve()
            fridrich_moves = len(list(solver.get_moves()))
    except TimeoutError:
        print("fridrich timeout")
        fridrich_moves = 2048
    return min(two_phase_moves, fridrich_moves)


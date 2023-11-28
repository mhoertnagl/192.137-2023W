from neighborhoods import Neighborhood
from solution import Solution


class VND:

    def __init__(self, nbhs: list[Neighborhood]):
        self.nbhs = nbhs

    def run(self, sol: Solution) -> Solution:
        i = 0
        while i < len(self.nbhs):
            new_sol = self.nbhs[i].choose(sol)
            if new_sol.get_value() < sol.get_value():
                sol = new_sol
                i = 0
            else:
                i += 1
        return sol

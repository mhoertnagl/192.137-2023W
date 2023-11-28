from neighborhoods import Neighborhood
from solution import Solution


class VND:

    def __init__(self, nbhds: list[Neighborhood]):
        self.nbhds = nbhds

    def run(self, sol: Solution) -> Solution:
        i = 0
        while i < len(self.nbhds):
            new_sol = self.nbhds[i].choose(sol)
            if new_sol.get_value() < sol.get_value():
                sol = new_sol
                i = 0
            else:
                i += 1
        return sol

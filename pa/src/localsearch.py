from neighborhoods import Neighborhood
from solution import Solution
from termination import Termination


# TODO: Termination condition.


class LocalSearch:

    def __init__(self, nbh: Neighborhood, ter: Termination):
        self.nbh = nbh
        self.ter = ter

    def run(self, sol: Solution) -> Solution:
        self.ter.init()
        while True:
            new_sol = self.nbh.choose(sol)
            if self.ter.done(sol, new_sol):
                break
            if new_sol.get_value() <= sol.get_value():
                sol = new_sol.copy()
        return sol


class LocalSearchTuning:

    def __init__(self, nbh: Neighborhood, ter: Termination):
        self.nbh = nbh
        self.ter = ter

    def run(self, sol: Solution) -> Solution:
        self.ter.init()
        c = 0
        f = []
        lo = 0
        while True:
            c += 1
            new_sol = self.nbh.choose(sol)
            if self.ter.done(sol, new_sol):
                break
            if new_sol.get_value() <= sol.get_value():
                sol = new_sol.copy()
                f.append(sol.get_value())
                lo = c
        return sol,c,f,lo
    
    
    
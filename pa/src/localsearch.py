from neighborhoods import Neighborhood
from solution import Solution

# TODO: Termination condition.


class LocalSearch:

    def __init__(self, nbh: Neighborhood, num_iterations: int):
        self.nbh = nbh
        self.num_iterations = num_iterations
        

    def run(self, sol: Solution) -> Solution:
        for _ in range(self.num_iterations):
            new_sol = self.nbh.choose(sol)
            if new_sol.get_value() <= sol.get_value():
                sol = new_sol
        return sol

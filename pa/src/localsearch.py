from neighborhoods import Neighborhood
from solution import Solution

# TODO: Termination condition.


class LocalSearch:

    def __init__(self,
                 sol: Solution,
                 nbh: Neighborhood,
                 num_iterations: int):
        self.sol = sol
        self.nbh = nbh
        self.num_iterations = num_iterations

    def run(self) -> Solution:
        for _ in range(self.num_iterations):
            new_sol = self.nbh.choose(self.sol)
            if new_sol.value <= self.sol.value:
                self.sol = new_sol
        return self.sol

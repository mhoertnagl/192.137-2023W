import math
import numpy as np

from neighborhoods import Neighborhood
from solution import Solution

# TODO: Termination condition.
# TODO: Equilibrium condition.


class Annealer:

    def __init__(self,
                 sol: Solution,
                 nbh: Neighborhood,
                 num_iterations: int,
                 alpha: float = 0.95):
        self.sol = sol
        self.nbh = nbh
        self.num_iterations = num_iterations
        self.alpha = alpha
        # Set initial temperature to the worst possible
        # value minus least possible value. The worst
        # value is the sum of all weights. Best is 0.
        self.temperature = sol.worst_value() - 0

    def run(self) -> Solution:
        while self.temperature > 1:
            for _ in range(self.num_iterations):
                new_sol = self.nbh.choose(self.sol)
                delta = new_sol.get_value() - self.sol.get_value()
                if self.metropolis(delta):
                    self.sol = new_sol
            self.cool_down()
            print(self.temperature)
        return self.sol

    def metropolis(self, delta: int) -> bool:
        if delta < 0:
            return True
        t = abs(delta) / self.temperature
        return np.random.random_sample() <= math.exp(-t)

    def cool_down(self):
        self.temperature *= self.alpha

import math
import numpy as np

from neighborhoods import Neighborhood
from solution import Solution


class Annealer:

    def __init__(self, sol: Solution, neighbors: Neighborhood, alpha: float = 0.95):
        self.sol = sol
        self.neighbors = neighbors
        self.alpha = alpha
        self.temperature = 0
        self.terminate = False

    def run(self) -> Solution:
        # while not self.__terminate:
        for _ in range(1000):
            # while True: # TODO: Equilibrium condition?
            for _ in range(1000):
                new_sol = self.neighbors.choose(self.sol)
                if self.metropolis(new_sol.value - self.sol.value):
                    self.sol = new_sol
            self.cool_down()
        return self.sol

    def metropolis(self, delta: int) -> bool:
        if delta < 0:
            return True
        t = abs(delta) / self.temperature
        return np.random.random_sample() <= math.exp(-t)

    def cool_down(self):
        self.temperature *= self.alpha
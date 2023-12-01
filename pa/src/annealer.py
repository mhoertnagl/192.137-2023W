import math
import numpy as np

from neighborhoods import Neighborhood
from solution import Solution
from termination import Termination

class Annealer:

    def __init__(self,
                 sol: Solution,
                 nbh: Neighborhood,
                 ter: Termination,
                 min_temp: float = 1,
                 alpha: float = 0.95):
        self.sol = sol
        self.nbh = nbh
        self.ter = ter
        self.min_temp = min_temp
        self.alpha = alpha
        # Set initial temperature to the worst possible
        # value minus least possible value. The worst
        # value is the sum of all weights. Best is 0.
        self.temperature = sol.worst_value() - 0

    def run(self) -> Solution:
        self.ter.init()
        while self.temperature > self.min_temp:
            while True:
                new_sol = self.nbh.choose(self.sol)
                if self.ter.done(self.sol, new_sol):
                    break
                delta = new_sol.get_value() - self.sol.get_value()
                if self.metropolis(delta):
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

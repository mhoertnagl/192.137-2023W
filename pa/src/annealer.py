import math
import numpy as np

from neighborhoods import Neighborhood
from solution import Solution


class Annealer:

    def __init__(self,
                 solution: Solution,
                 neighborhood: Neighborhood,
                 alpha: float = 0.95):
        self.__solution = solution
        self.__neighborhood = neighborhood
        self.__alpha = alpha
        self.__temperature = 0
        self.__terminate = False

    def run(self) -> Solution:
        # while not self.__terminate:
        for _ in range(1000):
            # while True: # TODO: Equilibrium condition?
            for _ in range(1000):
                new_solution, delta = self.__neighborhood.choose(self.__solution)
                if self.metropolis(delta):
                    self.__solution = new_solution
            self.cool_down()
        return self.__solution

    def metropolis(self, delta: int) -> bool:
        if delta < 0:
            return True
        t = abs(delta) / self.__temperature
        return np.random.random_sample() <= math.exp(-t)

    def cool_down(self):
        self.__temperature *= self.__alpha
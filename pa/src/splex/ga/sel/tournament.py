import math
import random
from abc import ABC

from splex import Problem, Solution
from splex.ga.population import Population

from splex.ga.sel import Selection


class TournamentSelection(Selection, ABC):

    def __init__(self, f: float, k: int = 2):
        # random.seed(time.time_ns())
        self._f = f
        self._k = k

    def select(self,
               problem: Problem,
               parents: Population,
               size: int) -> Population:
        winners: list[Solution] = []
        sz = math.ceil(self._f * size)
        for _ in range(sz):
            candidates = random.sample(parents.list(), self._k)
            winner = min(candidates, key=lambda c: c.value())
            winners.append(winner)
        return Population(winners)

    def __repr__(self):
        return f"Tournament Selection [f={self._f}, k={self._k}]"

    def __str__(self):
        return self.__repr__()

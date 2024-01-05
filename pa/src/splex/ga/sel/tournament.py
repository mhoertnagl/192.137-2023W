import random
from abc import ABC

from splex import Problem, Solution
from splex.ga.population import Population

from splex.ga.sel import Selection


class TournamentSelection(Selection, ABC):

    def __init__(self, size: int, k: int = 2):
        # random.seed(time.time_ns())
        self._size = size
        self._k = k

    def select(self,
               problem: Problem,
               parents: Population) -> Population:
        winners: list[Solution] = []
        for _ in range(self._size):
            candidates = random.sample(parents.list(), self._k)
            winner = min(candidates, key=lambda c: c.value())
            winners.append(winner)
        return Population(winners)

from abc import ABC

import numpy as np

from splex import Problem
from splex.ga.population import Population

from splex.ga.sel import Selection


class RouletteSelection(Selection, ABC):

    def __init__(self, size: int):
        self._size = size

    def select(self,
               problem: Problem,
               parents: Population) -> Population:
        sel = np.random.choice(
            parents.list(),
            size=self._size,
            replace=False,
            p=parents.probabilities()
        )
        return Population(sel)

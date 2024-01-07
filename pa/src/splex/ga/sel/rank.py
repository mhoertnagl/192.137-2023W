import math
from abc import ABC

import numpy as np

from splex import Problem
from splex.ga.population import Population

from splex.ga.sel import Selection


class RankSelection(Selection, ABC):

    def __init__(self, f: float):
        self._f = f

    def select(self,
               problem: Problem,
               parents: Population,
               size: int) -> Population:
        sz = math.ceil(self._f * size)
        return Population(parents[:sz])

    def __repr__(self):
        return f"Rank Selection [f={self._f}]"

    def __str__(self):
        return self.__repr__()

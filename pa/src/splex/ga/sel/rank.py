from abc import ABC

import numpy as np

from splex import Problem
from splex.ga import Population

from splex.ga.sel import Selection


class RankSelection(Selection, ABC):

    def __init__(self, size: int):
        self._size = size

    def select(self,
               problem: Problem,
               parents: Population) -> Population:
        return Population(parents[:self._size])

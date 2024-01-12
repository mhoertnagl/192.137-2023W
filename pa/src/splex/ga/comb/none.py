import math
from abc import ABC

from numpy.random import shuffle

from splex import Problem, Solution
from splex.ga.comb import Combiner
from splex.ga.population import Population


class NoCombiner(Combiner, ABC):

    def recombine(self,
                  problem: Problem,
                  selected: Population,
                  size: int) -> Population:
        return selected

    def __repr__(self):
        return f"No Combiner"

    def __str__(self):
        return self.__repr__()

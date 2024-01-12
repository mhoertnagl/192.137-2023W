import math
from abc import ABC

from numpy.random import shuffle

from splex import Problem, Solution
from splex.ga.comb import Combiner
from splex.ga.comb.utils import converge_parents
from splex.ga.population import Population


class ConvergeCombiner(Combiner, ABC):

    def __init__(self, f: float):
        self._f = f

    def recombine(self,
                  problem: Problem,
                  selected: Population,
                  size: int) -> Population:
        kids: list[Solution] = []
        sz = math.ceil(self._f * len(selected))
        for _ in range(sz):
            parents = selected.sample(2).list()
            kid = converge_parents(problem, parents[0], parents[1])
            kids.append(kid)
        return Population(kids)

    def __repr__(self):
        return f"Converge Combiner [f={self._f}]"

    def __str__(self):
        return self.__repr__()

import math
from abc import ABC

from splex import Problem
from splex.ga.population import Population

from splex.ga.rep import Replacer


class EliteReplacer(Replacer, ABC):

    def __init__(self, f: float):
        self._f = f

    def replace(self,
                problem: Problem,
                parents: Population,
                kids: Population,
                size: int) -> Population:
        # TODO: Sample parent elite?
        sz = math.ceil(self._f * size)
        elite, losers = parents.split(sz)
        rest = losers.join(kids).sample(size - sz)
        # if size - sz >= len(kids):
        #     return elite.join(kids)
        # rest = kids.sample(size - sz)
        return elite.join(rest)

    def __repr__(self):
        return f"Elite Replacement [f={self._f}]"

    def __str__(self):
        return self.__repr__()

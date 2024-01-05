from abc import ABC

from splex import Problem
from splex.ga.population import Population

from splex.ga.rep import Replacer


class EliteReplacer(Replacer, ABC):

    def __init__(self, elite_size: int):
        self._elite_size = elite_size

    def replace(self,
                problem: Problem,
                parents: Population,
                kids: Population,
                size: int) -> Population:
        # TODO: Sample parent elite?
        elite = parents.resize(self._elite_size)
        rest = kids.sample(size - self._elite_size)
        return elite.join(rest)

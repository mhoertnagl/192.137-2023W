from abc import ABC

from splex import Problem
from splex.ga.population import Population

from splex.ga.rep import Replacer


class BestReplacer(Replacer, ABC):

    def replace(self,
                problem: Problem,
                parents: Population,
                kids: Population,
                size: int) -> Population:
        return parents.join(kids).resize(size)
        # p = join_populations(parents, kids)
        # p.resize(size)
        # return p

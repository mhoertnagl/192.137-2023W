from abc import ABC

from numpy.random import shuffle

from splex import Problem, Solution
from splex.ga.comb import Combiner, pick_components
from splex.ga.population import Population


class ComponentsPickCombiner(Combiner, ABC):

    def __init__(self, k: int):
        self._k = k

    def recombine(self,
                  problem: Problem,
                  selected: Population) -> Population:
        kids: list[Solution] = []
        for _ in range(self._k):
            parents = selected.sample(2).list()
            kid = merge_parents(problem, parents[0], parents[1])
            kids.append(kid)
        return Population(kids)


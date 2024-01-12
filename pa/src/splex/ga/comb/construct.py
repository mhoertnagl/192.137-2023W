import math
from abc import ABC

from numpy.random import shuffle

from splex import Problem, Solution
from splex.ga.comb import Combiner
from splex.ga.population import Population


class ConstructCombiner(Combiner, ABC):

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
            kid = Solution(problem)
            cs1 = parents[0].frozen_components()
            cs2 = parents[1].frozen_components()
            for c in cs1.intersection(cs2):
                kid.add_edges(parents[0].edges(c))
            remainder: set[int] = set()
            for c in cs1.symmetric_difference(cs2):
                remainder = remainder.union(c)
            self.complete(problem, kid, list(remainder))
            kids.append(kid)
        return Population(kids)

    def complete(self,
                 problem: Problem,
                 solution: Solution,
                 remainder: list[int]):
        shuffle(remainder)
        for v in remainder:
            best_e, best_d = None, 0
            for c in solution.components():
                if v not in c:
                    cv = solution.component(v)
                    edges = [(u, w) for u in c for w in cv]
                    delta = solution.delta(edges, [])
                    if delta < best_d:
                        best_e = edges
                        best_d = delta
            if best_d < 0:
                solution.add_edges(best_e)

    def __repr__(self):
        return f"Converge Combiner [f={self._f}]"

    def __str__(self):
        return self.__repr__()

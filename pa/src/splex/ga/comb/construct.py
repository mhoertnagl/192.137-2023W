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
            best_e, best_d = None, None
            for c in solution.components():
                if v not in c:
                    edges, delta = self.find_edges_to_add(problem, solution, v, c)
                    if best_d is None or delta < best_d:
                        best_e = edges
                        best_d = delta
            if best_e is not None:
                solution.add_edges(best_e)

    def find_edges_to_add(self,
                          prob: Problem,
                          sol: Solution,
                          v: int,
                          c: set[int]):
        edges = []
        for u in c:
            edges.append((u, v))
        if len(c) > prob.s + 1:
            wedges = prob.weights_for_edges(edges)
            edges = [(u, v) for (w, u, v) in wedges[:len(c)+1-prob.s]]
        return edges, sol.delta(edges, [])

    def __repr__(self):
        return f"Converge Combiner [f={self._f}]"

    def __str__(self):
        return self.__repr__()

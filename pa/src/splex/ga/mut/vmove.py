import math
import random
import time
from abc import ABC
from random import sample, choice

from splex import Problem, Solution
from splex.ga.mut import Mutator


class VertexMoveMutation(Mutator, ABC):

    def __init__(self, fc: float, fv: float):
        """
        :param fc:  [0.0, 1.0] Fraction of mutated components.
        :param fv:  [0.0, 1.0] Fraction of mutated vertices per component.
        """
        # random.seed(time.time_ns())
        self._fc = fc
        self._fv = fv

    def mutate(self, problem: Problem, solution: Solution):
        ca = solution.components()
        if len(ca) < 2:
            self.swap(solution)
        else:
            self.move(solution)

    def swap(self, solution: Solution):
        ca = solution.components()
        c = list(ca[0])
        for _ in range(math.ceil(self._fc * len(ca))):
            v = choice(c)
            remv = [(w, v) for w in solution.neighbors(v)]
            for u in c:
                if u != v:
                    remu = [(w, u) for w in solution.neighbors(u)]
                    addv = [(u, w) for w in solution.neighbors(v)]
                    addu = [(v, w) for w in solution.neighbors(u)]
                    rem = remv + remu
                    add = addv + addu
                    if solution.delta(add, rem) < 0:
                        solution.remove_edges(rem)
                        solution.add_edges(add)
                        break

    def move(self, solution: Solution):
        ca = solution.components()
        for _ in range(math.ceil(self._fc * len(ca))):
            [c1, c2] = sample(ca, 2)
            for v in c1:
                rem = [(u, v) for u in solution.neighbors(v)]
                add = [(u, v) for u in c2 if u != v]
                if solution.delta(add, rem) < 0:
                    solution.remove_edges(rem)
                    solution.add_edges(add)
                    break

    def __repr__(self):
        return f"Vertex Move Mutation [fc={self._fc}, fv={self._fv}]"

    def __str__(self):
        return self.__repr__()


def sample_frac(population: list, fraction: float):
    k = math.ceil(fraction * len(population))
    return sample(population, k)

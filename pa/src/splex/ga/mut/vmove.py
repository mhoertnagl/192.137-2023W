import math
import random
import time
from abc import ABC
from random import sample

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
        for _ in range(math.ceil(self._fc * len(ca))):
            [c1, c2] = sample(ca, 2)
            for v in sample_frac(list(c1), self._fv):
                rem = [(u, v) for u in solution.neighbors(v)]
                add = [(u, v) for u in c2 if u != v]
                solution.remove_edges(rem)
                solution.add_edges(add)

    def __repr__(self):
        return f"Vertex Move Mutation [fc={self._fc}, fv={self._fv}]"

    def __str__(self):
        return self.__repr__()


def sample_frac(population: list, fraction: float):
    k = math.ceil(fraction * len(population))
    return sample(population, k)

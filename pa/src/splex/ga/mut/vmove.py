import math
import random
import time
from abc import ABC
from random import sample

from splex import Problem, Solution
from splex.ga.mut import Mutator


class VertexMoveMutation(Mutator, ABC):

    def __init__(self, rc: float, rv: float):
        # random.seed(time.time_ns())
        self._rc = rc
        self._rv = rv

    def mutate(self, problem: Problem, solution: Solution):
        ca = solution.components()
        for _ in range(math.ceil(self._rc * len(ca))):
            [c1, c2] = sample(ca, 2)
            for v in sample_frac(c1, self._rv):
                rem = [(u, v) for u in solution.neighbors(v)]
                add = [(u, v) for u in c2 if u != v]
                solution.remove_edges(rem)
                solution.add_edges(add)


def sample_frac(population, fraction: float):
    k = math.ceil(fraction * len(population))
    return sample(population, k)

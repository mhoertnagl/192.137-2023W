import math
import random
import time
from abc import ABC
from random import shuffle, sample

import numpy as np

from splex import Problem, Solution
from splex.ga.mut import Mutator


class VertexMoveMutation(Mutator, ABC):

    def __init__(self, rc: float, rv: float):
        # random.seed(time.time_ns())
        self._rc = rc
        self._rv = rv

    # def mutate(self, problem: Problem, solution: Solution):
    #     cs = c_sample(solution, self._rc)
    #     for i in range(len(cs)):
    #         j = (i+1) % len(cs)
    #         c1, c2 = cs[i], cs[j]
    #         for v in sample_frac(c1, self._rv):
    #             rem = [(u, v) for u in solution.neighbors(v)]
    #             add = [(u, v) for u in c2 if u != v]
    #             solution.remove_edges(rem)
    #             solution.add_edges(add)

    def mutate(self, problem: Problem, solution: Solution):
        ca = solution.components()
        for _ in range(math.ceil(self._rc * len(ca))):
            [c1, c2] = sample(ca, 2)
            for v in sample_frac(c1, self._rv):
                rem = [(u, v) for u in solution.neighbors(v)]
                add = [(u, v) for u in c2 if u != v]
                solution.remove_edges(rem)
                solution.add_edges(add)


# def c_sample(solution: Solution, fraction: float):
#     cs = solution.components()
#     return sample(cs, math.ceil(fraction * len(cs)))
#
#
# def c_shuffled(solution: Solution):
#     cs = solution.components()
#     shuffle(cs)
#     return cs
#
#
# def v_sample(n: int, fraction: float):
#     return sample(range(1, n+1), math.ceil(fraction * n))
#
#
# def v_shuffled(n: int):
#     vs = list(range(1, n+1))
#     shuffle(vs)
#     return vs


def sample_frac(population, fraction: float):
    k = math.ceil(fraction * len(population))
    return sample(population, k)

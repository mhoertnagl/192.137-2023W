from abc import ABC

import numpy as np

from benchy import ISolution
from splex import Problem


# class Components:
#
#     def __init__(self, n: int):
#         self._adjacent = np.zeros((n, n), dtype=int)
#
#     def connect(self, u: int, v: int):
#         pass
#
#     def disconnect(self, u: int, v: int):
#         pass
#
#     def component(self, v: int) -> set[int]:
#         return self._adjacent


class Solution(ISolution, ABC):

    def __init__(self, problem: Problem):
        self._problem = problem

    def value(self) -> int | float:
        pass
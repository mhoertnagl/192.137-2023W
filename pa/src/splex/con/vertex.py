from abc import ABC

from .construction import Construction
from splex import Problem, Solution


class VertexConstruction(Construction, ABC):

    def construct(self, problem: Problem) -> Solution:
        pass

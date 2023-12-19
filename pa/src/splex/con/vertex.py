from abc import ABC

from .construction import Construction
from splex import SPlexProblem, SPlexSolution


class VertexConstruction(Construction, ABC):

    def construct(self, problem: SPlexProblem) -> SPlexSolution:
        pass

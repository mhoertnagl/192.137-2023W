from abc import ABC

from splex import SPlexSolution
from splex.ga.mut import Mutator


class VertexMoveMutation(Mutator, ABC):

    def mutate(self, solution: SPlexSolution) -> SPlexSolution:
        pass

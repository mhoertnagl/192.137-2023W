from abc import ABC

from splex import Solution
from splex.ga.mut import Mutator


class VertexMoveMutation(Mutator, ABC):

    def mutate(self, solution: Solution) -> Solution:
        pass

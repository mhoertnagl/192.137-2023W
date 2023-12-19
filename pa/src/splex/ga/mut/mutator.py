from abc import ABC, abstractmethod

from splex import SPlexSolution


class Mutator(ABC):

    @abstractmethod
    def mutate(self, solution: SPlexSolution) -> SPlexSolution:
        pass

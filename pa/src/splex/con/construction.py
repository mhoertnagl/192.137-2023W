from abc import ABC, abstractmethod

from splex import SPlexProblem, SPlexSolution


class Construction(ABC):

    @abstractmethod
    def construct(self, problem: SPlexProblem) -> SPlexSolution:
        pass

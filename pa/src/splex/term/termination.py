from abc import ABC, abstractmethod

from splex import SPlexSolution


class Termination(ABC):

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def done(self, old: SPlexSolution, new: SPlexSolution) -> bool:
        pass

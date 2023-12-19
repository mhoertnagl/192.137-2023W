from abc import ABC, abstractmethod

from splex import Solution


class Termination(ABC):

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def done(self, old: Solution, new: Solution) -> bool:
        pass

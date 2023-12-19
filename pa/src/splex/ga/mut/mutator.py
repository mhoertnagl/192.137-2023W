from abc import ABC, abstractmethod

from splex import Solution


class Mutator(ABC):

    @abstractmethod
    def mutate(self, solution: Solution) -> Solution:
        pass

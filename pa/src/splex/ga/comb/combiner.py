from abc import ABC, abstractmethod

from splex import Problem
from splex.ga import Population


class Combiner(ABC):

    @abstractmethod
    def recombine(self,
                problem: Problem,
                selected: Population) -> Population:
        pass

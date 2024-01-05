from abc import ABC, abstractmethod

from splex import Problem
from splex.ga.population import Population


class Selection(ABC):

    @abstractmethod
    def select(self,
               problem: Problem,
               parents: Population) -> Population:
        pass

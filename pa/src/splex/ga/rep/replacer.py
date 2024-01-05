from abc import ABC, abstractmethod

from splex import Problem
from splex.ga.population import Population


class Replacer(ABC):

    @abstractmethod
    def replace(self,
                problem: Problem,
                parents: Population,
                kids: Population,
                size: int) -> Population:
        pass

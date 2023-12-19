from abc import ABC, abstractmethod

from .problem import IProblem
from .solution import ISolution


class Fixture(ABC):

    @abstractmethod
    def run(self, problem: IProblem, args: dict[str, any]) -> ISolution:
        pass

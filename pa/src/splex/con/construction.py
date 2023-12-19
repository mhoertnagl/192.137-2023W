from abc import ABC, abstractmethod

from splex import Problem, Solution


class Construction(ABC):

    @abstractmethod
    def construct(self, problem: Problem) -> Solution:
        pass

from abc import ABC, abstractmethod

from splex import Problem, Solution


class Mutator(ABC):

    @abstractmethod
    def mutate(self, problem: Problem, solution: Solution):
        pass

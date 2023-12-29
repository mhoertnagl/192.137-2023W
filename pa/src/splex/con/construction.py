from abc import ABC, abstractmethod

from splex import Problem, Solution


class Construction(ABC):

    @abstractmethod
    def construct(self, problem: Problem) -> Solution:
        pass

    def construct_many(self, problem: Problem, size: int) -> list[Solution]:
        solutions = []
        for _ in range(size):
            solution = self.construct(problem)
            solutions.append(solution)
        return solutions
from abc import ABC, abstractmethod

from solution import Solution


class Termination(ABC):

    @abstractmethod
    def done(self, sol: Solution, new_sol: Solution) -> bool:
        pass


class IterationTermination(Termination, ABC):

    def __init__(self, n: int):
        self.i = 0
        self.n = n

    def done(self, _sol: Solution, _new_sol: Solution) -> bool:
        if self.i >= self.n:
            return True
        self.i += 1
        return False


class ImprovementTermination(Termination, ABC):

    def __init__(self, percent: float):
        self.limit = percent / 100

    def done(self, sol: Solution, new_sol: Solution) -> bool:
        f1, f0 = new_sol.get_value(), sol.get_value()
        return 1 - (f1 / f0) < self.limit
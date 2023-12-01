from abc import ABC, abstractmethod

from solution import Solution


class Termination(ABC):

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def done(self, sol: Solution, new_sol: Solution) -> bool:
        pass


class IterationTermination(Termination, ABC):

    def __init__(self, n: int = 1000):
        self.i = 0
        self.n = n

    def init(self):
        self.i = 0

    def done(self, _sol: Solution, _new_sol: Solution) -> bool:
        if self.i >= self.n:
            return True
        self.i += 1
        return False


class ImprovementTermination(Termination, ABC):

    def __init__(self, percent: float = 3):
        self.limit = percent / 100

    def done(self, sol: Solution, new_sol: Solution) -> bool:
        f1, f0 = new_sol.get_value(), sol.get_value()
        return 1 - (f1 / f0) < self.limit


class IterationAndImprovementTermination(Termination, ABC):

    def __init__(self, n: int = 1000, percent: float = 3):
        self.i = 0
        self.n = n
        self.limit = percent / 100

    def init(self):
        self.i = 0

    def done(self, sol: Solution, new_sol: Solution) -> bool:                
        if self.i >= self.n:
            return True        
        f1, f0 = new_sol.get_value(), sol.get_value()
        if 1 - (f1 / f0) < self.limit:
            self.i += 1
        else:
            self.i = 0
        return False
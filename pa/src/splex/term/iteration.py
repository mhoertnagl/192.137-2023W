from abc import ABC

from splex import Solution
from splex.term import Termination


class IterationTermination(Termination, ABC):

    def __init__(self, n: int = 1000):
        self._i = 0
        self._n = n

    def init(self):
        self._i = 0

    def done(self, old: Solution, new: Solution) -> bool:
        if self._i >= self._n:
            return True
        self._i += 1
        return False

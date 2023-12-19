from abc import ABC

from splex import Solution
from splex.term import Termination


class ImprovementTermination(Termination, ABC):

    def __init__(self, percent: float = 3, window: int = 100):
        self._i = 0
        self._limit = percent / 100
        self._window = window

    def init(self):
        self._i = 0

    def done(self, old: Solution, new: Solution) -> bool:
        f1, f0 = new.value(), old.value()
        if 1 - (f1 / f0) > self._limit:
            # Change is bigger than the limit.
            # Reset the counter.
            self._i = 0
        elif self._i >= self._window:
            # Counter reached window. There has not
            # been a significant change greater than
            # limit for window iterations.
            return True
        return False

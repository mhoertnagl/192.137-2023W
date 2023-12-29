import random

import numpy as np

from splex import Solution


class Population:

    def __init__(self, initial: list[Solution] | None = None):
        if initial is None:
            self._list: list[Solution] = []
        else:
            self._list = initial
        self._sort()

    def append(self, solution: Solution):
        self._list.append(solution)
        self._sort()
        return self

    def extend(self, solutions: list[Solution]):
        self._list.extend(solutions)
        self._sort()
        return self

    def join(self, other):
        self.extend(other.list())
        return self

    def resize(self, size: int):
        if size <= 0 or size >= len(self._list):
            return self
        return Population(self._list[:size])

    # def roulette(self, size: int):
    #     sel = np.random.choice(
    #         self._list,
    #         size=size,
    #         replace=False,
    #         p=self.probabilities()
    #     )
    #     return Population(sel)

    def sample(self, size: int):
        sample = random.sample(self._list, size)
        return Population(sample)

    def best(self) -> Solution:
        return self._list[0]

    def list(self):
        return self._list

    def probabilities(self):
        total = self._total()
        return [s.value() / total for s in self._list]

    def _total(self) -> int | float:
        return sum([s.value() for s in self._list])

    def _sort(self):
        self._list.sort(key=lambda s: s.value(), reverse=True)

    def __getitem__(self, item):
        return self._list.__getitem__(item)

    def __iter__(self):
        return self._list.__iter__()

    def __len__(self):
        return self._list.__len__()


def join_populations(p1: Population, p2: Population) -> Population:
    return Population(p1.list() + p2.list())
    # p = Population()
    # p.extend(p1.list())
    # p.extend(p2.list())
    # return p

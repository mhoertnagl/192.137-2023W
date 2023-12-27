from splex import Solution


class Population:

    def __init__(self):
        self._list: list[Solution] = []

    def append(self, solution: Solution):
        self._list.append(solution)
        self._sort()

    def extend(self, solutions: list[Solution]):
        self._list.extend(solutions)
        self._sort()

    def best(self) -> Solution:
        return self._list[0]
        # best: Solution | None = None
        # for individual in self:
        #     if best is None or individual.is_better_than(best):
        #         best = individual
        # return best

    def _sort(self):
        self._list.sort(key=lambda s: s.value(), reverse=True)

    def __getitem__(self, item):
        return self._list.__getitem__(item)

    def __iter__(self):
        return self._list.__iter__()

    def __len__(self):
        return self._list.__len__()

from concurrent.futures import ProcessPoolExecutor, wait, ALL_COMPLETED

from benchy import *


class Testbench:

    def __init__(self):
        self._problems: list[Problem] = list()
        self._haresses: list[Harness] = list()
        self._executor = ProcessPoolExecutor()

    def add_problem(self, problem: Problem):
        self._problems.append(problem)
        return self

    def add_problems(self, problems: list[Problem]):
        for problem in problems:
            self.add_problem(problem)
        return self

    def add_harness(self, harness: Harness):
        self._haresses.append(harness)
        return self

    def run(self) -> Benchmark:
        pass


def run_task():
    pass

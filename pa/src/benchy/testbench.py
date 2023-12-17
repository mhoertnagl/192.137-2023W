from concurrent.futures import ProcessPoolExecutor, wait, ALL_COMPLETED
# import smac
from benchy import *


class Testbench:

    def __init__(self):
        self._plugins: list[Plugin] = list()
        self._problems: list[Problem] = list()
        self._haresses: list[Harness] = list()
        self._executor = ProcessPoolExecutor()

    def add_plugin(self, plugin: Plugin):
        self._plugins.append(plugin)
        return self

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

    def run(self):
        for plugin in self._plugins:
            plugin.testbench_before(self)
        for problem in self._problems:
            self.run_problem(problem)
        for plugin in self._plugins:
            plugin.testbench_after(self)

    def run_problem(self, problem: Problem):
        for plugin in self._plugins:
            plugin.problem_before(self, problem)
        for harness in self._haresses:
            self.run_harness(problem, harness)
        for plugin in self._plugins:
            plugin.problem_after(self, problem)

    def run_harness(self, problem: Problem, harness: Harness):
        for plugin in self._plugins:
            plugin.harness_before(self, problem, harness)
        for fixture in harness:
            print(fixture, "\n")
        for plugin in self._plugins:
            plugin.harness_after(self, problem, harness)


def run_task():
    pass

# Hooks for all stages of a run -> console logger, file logger, solution file export, csv statistics export

from abc import ABC, abstractmethod

import numpy as np

from problem import Problem
from reader import Reader
from solution import Solution


class Benchmark(ABC):

    @abstractmethod
    def name(self) -> str:
        return ""

    @abstractmethod
    def run(self, problem: Problem) -> Solution:
        pass


class Result:

    def __init__(self, problem: Problem, benchmark: Benchmark):
        self.problem = problem
        self.benchmark = benchmark
        self.best_solution: Solution | None = None
        self.values: list[int] = []

    def add_solution(self, solution: Solution):
        cur_best = self.best_solution.get_value()
        new_best = solution.get_value()
        if self.best_solution is None or new_best < cur_best:
            self.best_solution = solution
        self.values.append(new_best)

    def get_best_solution(self):
        return self.best_solution

    def get_average_value(self):
        return np.average(self.values)

    def get_std_deviation(self):
        return np.std(self.values)


class Testbench:

    def __init__(self, n: int = 30):
        self.n = n
        self.reader = Reader()
        self.filenames: list[str] = []
        self.benchmarks: list[Benchmark] = []

    def add_filename(self, filename: str):
        self.filenames.append(filename)

    def add_benchmark(self, benchmark: Benchmark):
        self.benchmarks.append(benchmark)

    def run(self) -> list[Result]:
        results: list[Result] = []
        for filename in self.filenames:
            problem = self.reader.read(filename)
            for benchmark in self.benchmarks:
                result = Result(problem, benchmark)
                for i in range(1, self.n+1):
                    solution = benchmark.run(problem)
                    result.add_solution(solution)
        return results

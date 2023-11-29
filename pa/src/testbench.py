import os
from abc import ABC, abstractmethod

import time
from concurrent.futures import ProcessPoolExecutor
from io import StringIO
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
        self.runtimes: list[float] = []
        self.values: list[int] = []

    def add_solution(self, solution: Solution, runtime: float):
        new_best = solution.get_value()
        if self.best_solution is None:
            self.best_solution = solution
        elif new_best < self.best_solution.get_value():
            self.best_solution = solution
        self.runtimes.append(runtime)
        self.values.append(new_best)

    def get_best_solution(self):
        return self.best_solution

    def get_average_runtime(self):
        return np.average(self.runtimes)

    def get_std_deviation_runtime(self):
        return np.std(self.runtimes)

    def get_average_value(self):
        return np.average(self.values)

    def get_std_deviation_value(self):
        return np.std(self.values)

    def __str__(self):
        s = StringIO()
        s.write(f"Problem:         {self.problem.name}\n")
        s.write(f"Best Value:      {self.best_solution.get_value()}\n")
        s.write(f"Avg Value:       {self.get_average_value()}\n")
        s.write(f"Std Dev Value:   {self.get_std_deviation_value()}\n")
        s.write(f"Avg Runtime:     {self.get_average_runtime() * 1000:.0f}\n")
        s.write(f"Std Dev Runtime: {self.get_std_deviation_runtime() * 1000:.0f}\n")
        return s.getvalue()

    def write(self, out_dir: str):
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"{self.benchmark.name()}.txt")
        with open(filename, "w") as file:
            file.write(self.__str__())


class Testbench:

    def __init__(self, out_dir: str = "../res", n: int = 30):
        self.out_dir = out_dir
        self.n = n
        self.reader = Reader()
        self.filenames: list[str] = []
        self.benchmarks: list[Benchmark] = []

    def add_filename(self, filename: str):
        self.filenames.append(filename)

    def add_directory(self, path: str):
        for item in os.listdir(path):
            filename = os.path.join(path, item)
            if os.path.isfile(filename):
                self.add_filename(filename)

    def add_benchmark(self, benchmark: Benchmark):
        self.benchmarks.append(benchmark)

    def run(self) -> list[Result]:
        run_dir = time.strftime("%Y%m%d-%H%M%S")
        out_dir = os.path.join(self.out_dir, run_dir)
        print(f"Running testbench '{run_dir}' (n = {self.n})")
        print("=" * 74)
        results: list[Result] = []
        start_time = time.time()
        for filename in self.filenames:
            problem = self.reader.read(filename)
            print(f"Problem '{problem.name}'")
            print("-" * 74)
            for benchmark in self.benchmarks:
                result = self.run_benchmark(problem, benchmark)
                results.append(result)
                self.__write(out_dir, result)
                print(result)
        elapsed_time = time.time() - start_time
        print("=" * 74)
        print(f"Testbench run in {elapsed_time * 1000:.0f}\n")
        return results

    def run_benchmark(self, problem: Problem, benchmark: Benchmark) -> Result:
        print(f"Benchmark '{benchmark.name()}'")
        result = Result(problem, benchmark)
        for i in range(1, self.n+1):
            start_time = time.time()
            solution = benchmark.run(problem)
            elapsed_time = time.time() - start_time
            result.add_solution(solution, elapsed_time)
        return result

    def __write(self, out_dir: str, result: Result):
        bm_dir = os.path.join(out_dir, f"{result.benchmark.name()}")
        os.makedirs(bm_dir, exist_ok=True)
        result.best_solution.write(bm_dir)
        result.write(bm_dir)


class ParallelTestbench:

    def __init__(self, out_dir: str = "../res", n: int = 30):
        self.out_dir = out_dir
        self.n = n
        self.executor = ProcessPoolExecutor()
        self.reader = Reader()
        self.filenames: list[str] = []
        self.benchmarks: list[Benchmark] = []

    def add_filename(self, filename: str):
        self.filenames.append(filename)

    def add_directory(self, path: str):
        for item in os.listdir(path):
            filename = os.path.join(path, item)
            if os.path.isfile(filename):
                self.add_filename(filename)

    def add_benchmark(self, benchmark: Benchmark):
        self.benchmarks.append(benchmark)

    def run(self) -> list[Result]:
        run_dir = time.strftime("%Y%m%d-%H%M%S")
        out_dir = os.path.join(self.out_dir, run_dir)
        results: list[Result] = []
        for filename in self.filenames:
            problem = self.reader.read(filename)
            for benchmark in self.benchmarks:
                result = Result(problem, benchmark)
                for i in range(1, self.n+1):
                    task = self.executor.submit(self.run_one, problem, benchmark)
                    solution, elapsed_time = task.result()
                    result.add_solution(solution, elapsed_time)
                results.append(result)
                self.__write(out_dir, result)
                print(result)
        return results

    def run_one(self, problem: Problem, benchmark: Benchmark):
        start_time = time.time()
        solution = benchmark.run(problem)
        elapsed_time = time.time() - start_time
        return solution, elapsed_time

    def __write(self, out_dir: str, result: Result):
        bm_dir = os.path.join(out_dir, f"{result.benchmark.name()}")
        os.makedirs(bm_dir, exist_ok=True)
        result.best_solution.write(bm_dir)
        result.write(bm_dir)

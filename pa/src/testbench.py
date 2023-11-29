import os
from abc import ABC, abstractmethod

import time
from concurrent.futures import ProcessPoolExecutor, wait, ALL_COMPLETED
from io import StringIO
from typing import TextIO

import numpy as np

from problem import Problem
from reader import Reader
from solution import Solution


class Benchmark(ABC):

    def __init__(self, is_deterministic=False):
        self.is_deterministic = is_deterministic
        self.results: list[Result] = []

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
        s.write(f"Problem Worst:   {self.problem.worst_value()}\n")
        s.write(f"Best Value:      {self.best_solution.get_value()}\n")
        s.write(f"Avg Value:       {self.get_average_value()}\n")
        s.write(f"Std Dev Value:   {self.get_std_deviation_value()}\n")
        s.write(f"Avg Runtime:     {self.get_average_runtime() * 1000:.0f} ms\n")
        s.write(f"Std Dev Runtime: {self.get_std_deviation_runtime() * 1000:.0f} ms")
        return s.getvalue()

    def write(self, out_dir: str):
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"{self.benchmark.name()}.txt")
        with open(filename, "w") as file:
            file.write(self.__str__())


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

    def run(self):
        run_dir = time.strftime("%Y%m%d-%H%M%S")
        out_dir = os.path.join(self.out_dir, run_dir)
        print(f"Testbench '{run_dir}' (n = {self.n})")
        start_time = time.time()
        table = Table(self.benchmarks)
        for filename in self.filenames:
            problem = self.reader.read(filename)
            print("=" * 60)
            print(f"Problem '{problem.name}'")
            print("=" * 60)
            table.add_problem(problem)
            for benchmark in self.benchmarks:
                result = self.run_benchmark(problem, benchmark)
                benchmark.results.append(result)
                self.__write(out_dir, result)
                table.add_result(problem, benchmark, result)
                print(result)
                print("-" * 60)
        elapsed_time = time.time() - start_time
        table.write(out_dir)
        print("=" * 60)
        print(f"Testbench run in {elapsed_time * 1000:.0f} ms\n")
        self.executor.shutdown(cancel_futures=True)

    def run_benchmark(self, problem: Problem, benchmark: Benchmark) -> Result:
        print(f"Benchmark '{benchmark.name()}'")
        print("-" * 60)
        result = Result(problem, benchmark)
        tasks = []
        # Run deterministic test benches only once.
        n = 1 if benchmark.is_deterministic else self.n
        for _ in range(0, n):
            task = self.executor.submit(run_benchmark_as_task, problem, benchmark)
            tasks.append(task)
        done, not_done = wait(tasks, return_when=ALL_COMPLETED, timeout=15*60)
        for task in done:
            solution, elapsed_time = task.result()
            result.add_solution(solution, elapsed_time)
        if len(not_done) > 0:
            print(f"Could not complete {len(not_done)} runs within 15 min.")
        return result

    def __write(self, out_dir: str, result: Result):
        bm_dir = os.path.join(out_dir, f"{result.benchmark.name()}")
        os.makedirs(bm_dir, exist_ok=True)
        result.best_solution.write(bm_dir)


def run_benchmark_as_task(problem: Problem, benchmark: Benchmark):
    start_time = time.time()
    solution = benchmark.run(problem)
    elapsed_time = time.time() - start_time
    return solution, elapsed_time


class Table:

    def __init__(self, benchmarks: list[Benchmark]):
        self.n = 0
        self.problems: list[Problem] = []
        self.benchmarks = benchmarks
        self.results: dict[(str, str), Result] = dict()

    def add_problem(self, problem: Problem):
        self.problems.append(problem)

    def add_result(self, problem: Problem, benchmark: Benchmark, result: Result):
        self.results[(problem.name, benchmark.name())] = result

    def write(self, out_dir: str):
        filename = os.path.join(out_dir, f"table.txt")
        os.makedirs(out_dir, exist_ok=True)
        with open(filename, "w") as file:
            self.__write_best_values(file)
            self.__write_average_values(file)
            self.__write_std_values(file)
            self.__write_average_runtime(file)
            self.__write_std_runtime(file)

    def __write_best_values(self, file: TextIO):
        file.write("\\begin{tabular}{|l")
        file.write("|c" * len(self.benchmarks))
        file.write("|}\n")
        file.write("\\hline\n")
        for benchmark in self.benchmarks:
            file.write(f"& {benchmark.name()} ")
        file.write("\\\\ \\hline\n")
        for problem in self.problems:
            name = problem.name.replace('_', '\\_')
            file.write(f" {name} ")
            for benchmark in self.benchmarks:
                result = self.results[(problem.name, benchmark.name())]
                file.write(f"& {result.best_solution.get_value()} ")
            file.write("\\\\ \\hline\n")
        file.write("\\end{tabular}\n")

    def __write_average_values(self, file: TextIO):
        file.write("\\begin{tabular}{|l")
        file.write("|c" * len(self.benchmarks))
        file.write("|}\n")
        file.write("\\hline\n")
        for benchmark in self.benchmarks:
            file.write(f"& {benchmark.name()} ")
        file.write("\\\\ \\hline\n")
        for problem in self.problems:
            name = problem.name.replace('_', '\\_')
            file.write(f" {name} ")
            for benchmark in self.benchmarks:
                result = self.results[(problem.name, benchmark.name())]
                file.write(f"& {result.get_average_value():.2f} ")
            file.write("\\\\ \\hline\n")
        file.write("\\end{tabular}\n")

    def __write_std_values(self, file: TextIO):
        file.write("\\begin{tabular}{|l")
        file.write("|c" * len(self.benchmarks))
        file.write("|}\n")
        file.write("\\hline\n")
        for benchmark in self.benchmarks:
            file.write(f"& {benchmark.name()} ")
        file.write("\\\\ \\hline\n")
        for problem in self.problems:
            name = problem.name.replace('_', '\\_')
            file.write(f" {name} ")
            for benchmark in self.benchmarks:
                result = self.results[(problem.name, benchmark.name())]
                file.write(f"& {result.get_std_deviation_value():.2f} ")
            file.write("\\\\ \\hline\n")
        file.write("\\end{tabular}\n")

    def __write_average_runtime(self, file: TextIO):
        file.write("\\begin{tabular}{|l")
        file.write("|c" * len(self.benchmarks))
        file.write("|}\n")
        file.write("\\hline\n")
        for benchmark in self.benchmarks:
            file.write(f"& {benchmark.name()} ")
        file.write("\\\\ \\hline\n")
        for problem in self.problems:
            name = problem.name.replace('_', '\\_')
            file.write(f" {name} ")
            for benchmark in self.benchmarks:
                result = self.results[(problem.name, benchmark.name())]
                file.write(f"& {result.get_average_runtime() * 1000:.0f} ms ")
            file.write("\\\\ \\hline\n")
        file.write("\\end{tabular}\n")

    def __write_std_runtime(self, file: TextIO):
        file.write("\\begin{tabular}{|l")
        file.write("|c" * len(self.benchmarks))
        file.write("|}\n")
        file.write("\\hline\n")
        for benchmark in self.benchmarks:
            file.write(f"& {benchmark.name()} ")
        file.write("\\\\ \\hline\n")
        for problem in self.problems:
            name = problem.name.replace('_', '\\_')
            file.write(f" {name} ")
            for benchmark in self.benchmarks:
                result = self.results[(problem.name, benchmark.name())]
                file.write(f"& {result.get_std_deviation_runtime() * 1000:.0f} ms ")
            file.write("\\\\ \\hline\n")
        file.write("\\end{tabular}\n")

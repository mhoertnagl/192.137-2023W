import time
from concurrent.futures import ProcessPoolExecutor, wait, ALL_COMPLETED
# import smac
from .problem import IProblem
from .solution import ISolution
from .instance import Instance
from .harness import Harness


class ProblemContext:

    def __init__(self, testbench, problem: IProblem):
        self._testbench = testbench
        self._problem = problem

    def testbench(self):
        return self._testbench

    def problem(self):
        return self._problem


class HarnessContext:

    def __init__(self, ctx: ProblemContext, harness: Harness):
        self._testbench = ctx.testbench()
        self._problem = ctx.problem()
        self._harness = harness

    def testbench(self):
        return self._testbench

    def problem(self):
        return self._problem

    def harness(self):
        return self._harness


class InstanceContext:

    def __init__(self, ctx: HarnessContext, instance: Instance):
        self._testbench = ctx.testbench()
        self._problem = ctx.problem()
        self._harness = ctx.harness()
        self._instance = instance

    def testbench(self):
        return self._testbench

    def problem(self):
        return self._problem

    def harness(self):
        return self._harness

    def instance(self):
        return self._instance


class BeforeInstanceContext:

    def __init__(self, ctx: InstanceContext, run: int):
        self._testbench = ctx.testbench()
        self._problem = ctx.problem()
        self._harness = ctx.harness()
        self._instance = ctx.instance()
        self._run = run

    def testbench(self):
        return self._testbench

    def problem(self):
        return self._problem

    def harness(self):
        return self._harness

    def instance(self):
        return self._instance

    def run(self):
        return self._run


class AfterInstanceContext:

    def __init__(self,
                 ctx: InstanceContext,
                 run: int,
                 solution: ISolution,
                 bests: list[int | float],
                 elapsed_time: float):
        self._testbench = ctx.testbench()
        self._problem = ctx.problem()
        self._harness = ctx.harness()
        self._instance = ctx.instance()
        self._run = run
        self._solution = solution
        self._bests = bests
        self._elapsed_time = elapsed_time

    def testbench(self):
        return self._testbench

    def problem(self):
        return self._problem

    def harness(self):
        return self._harness

    def instance(self):
        return self._instance

    def run(self):
        return self._run

    def solution(self):
        return self._solution

    def bests(self):
        return self._bests

    def elapsed_time(self):
        return self._elapsed_time


class Testbench:

    def __init__(self):
        self._plugins: list = list()
        self._problems: list[IProblem] = list()
        self._haresses: list[Harness] = list()
        self._executor = ProcessPoolExecutor()

    def add_plugin(self, plugin):
        self._plugins.append(plugin)
        return self

    def add_problem(self, problem: IProblem):
        self._problems.append(problem)
        return self

    def add_problems(self, problems: list[IProblem]):
        for problem in problems:
            self.add_problem(problem)
        return self

    def add_harness(self, harness: Harness):
        self._haresses.append(harness)
        return self

    def run(self):
        self._run_problems()
        self._executor.shutdown(cancel_futures=True)

    def _run_problems(self):
        for plugin in self._plugins:
            plugin.testbench_before(self)
        for problem in self._problems:
            ctx2 = ProblemContext(self, problem)
            self._run_problem(ctx2)
        for plugin in self._plugins:
            plugin.testbench_after(self)

    def _run_problem(self, ctx: ProblemContext):
        for plugin in self._plugins:
            plugin.problem_before(ctx)
        for harness in self._haresses:
            ctx2 = HarnessContext(ctx, harness)
            self._run_harness(ctx2)
        for plugin in self._plugins:
            plugin.problem_after(ctx)

    def _run_harness(self, ctx: HarnessContext):
        for plugin in self._plugins:
            plugin.harness_before(ctx)
        for instance in ctx.harness():
            ctx2 = InstanceContext(ctx, instance)
            self._run_batch(ctx2)
        for plugin in self._plugins:
            plugin.harness_after(ctx)

    def _run_batch(self, ctx: InstanceContext):
        tasks = []
        # Run the instance multiple times in parallel.
        for run in range(ctx.harness().repetitions()):
            ctx2 = BeforeInstanceContext(ctx, run)
            for plugin in self._plugins:
                plugin.instance_before(ctx2)
            task = self._executor.submit(
                run_task,
                ctx2.instance(),
                ctx2.problem(),
                ctx2.run()
            )
            tasks.append(task)
        # Wait for all the parallel runs to finish.
        done, not_done = wait(tasks, return_when=ALL_COMPLETED)
        # # Print an error message if some task could not be finished.
        # d, n = len(done), len(not_done)
        # if n > 0:
        #     print(f"Timeout: could not complete {n} out of {d+n} runs.")
        # Process completed tasks.
        for task in done:
            solution, bests, elapsed_time, run = task.result()
            ctx2 = AfterInstanceContext(ctx, run, solution, bests, elapsed_time)
            for plugin in self._plugins:
                plugin.instance_after(ctx2)


def run_task(instance, problem, run):
    start_time = time.time()
    solution, bests = instance.run(problem)
    elapsed_time = time.time() - start_time
    return solution, bests, elapsed_time, run

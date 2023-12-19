import time
from concurrent.futures import ProcessPoolExecutor, wait, ALL_COMPLETED
# import smac
from benchy import *
from benchy.plugins.plugin import Plugin


class Testbench:

    def __init__(self):
        self._plugins: list[Plugin] = list()
        self._problems: list[IProblem] = list()
        self._haresses: list[Harness] = list()
        self._executor = ProcessPoolExecutor()

    def add_plugin(self, plugin: Plugin):
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

    # TODO: swap problem and harness order?
    def run(self):
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
            task = self._run_instance(ctx2)
            tasks.append(task)
        # Wait for all the parallel runs to finish.
        done, not_done = wait(tasks, return_when=ALL_COMPLETED)
        self._finish_batch(ctx, done, not_done)

    def _run_instance(self, ctx: BeforeInstanceContext):
        for plugin in self._plugins:
            plugin.instance_before(ctx)
        return self._executor.submit(run_task, ctx)

    def _finish_batch(self, ctx, done, not_done):
        d, n = len(done), len(not_done)
        if n > 0:
            print(f"Timeout: could not complete {n} of {d+n} runs.")
        for task in done:
            self._finish_instance(ctx, task)

    def _finish_instance(self, ctx: InstanceContext, task):
        solution, elapsed_time, run = task.result()
        ctx2 = AfterInstanceContext(ctx, run, solution, elapsed_time)
        for plugin in self._plugins:
            plugin.instance_after(ctx2)


def run_task(ctx: BeforeInstanceContext):
    start_time = time.time()
    solution = ctx.instance().run(ctx.problem())
    elapsed_time = time.time() - start_time
    return solution, elapsed_time, ctx.run()

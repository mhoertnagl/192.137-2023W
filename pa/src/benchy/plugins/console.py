from abc import ABC

from benchy.testbench import *
from benchy.plugins.plugin import Plugin

# import threading
# https://rich.readthedocs.io/en/latest/


class ConsoleLogPlugin(Plugin, ABC):

    def __init__(self):
        self._counter = 0

    def testbench_before(self, testbench: Testbench):
        print("=" * 60)
        print(f"Running testbench")
        print("=" * 60)

    def testbench_after(self, testbench: Testbench):
        print("=" * 60)
        print(f"Testbench completed")
        print("=" * 60)

    def problem_before(self, ctx: ProblemContext):
        print("-" * 60)
        print(f"Running Problem '{ctx.problem().name()}'")
        print("-" * 60)

    def problem_after(self, ctx: ProblemContext):
        print("-" * 60)
        print(f"Problem '{ctx.problem().name()}' completed")
        print("-" * 60)

    def harness_before(self, ctx: HarnessContext):
        self._counter = 0
        print(f"Running Harness '{ctx.harness().name()}'")

    def harness_after(self, ctx: HarnessContext):
        print()
        print(f"Harness '{ctx.harness().name()}' completed")

    def instance_before(self, ctx: BeforeInstanceContext):
        pass

    def instance_after(self, ctx: AfterInstanceContext):
        self._counter += 1
        progress = f"{self._counter} of {ctx.harness().size()}"
        args = ctx.instance().args()
        elapsed_time = f"{ctx.elapsed_time() * 1000:.0f} ms"
        construction = ctx.bests()[0]
        value = ctx.solution().value()
        feasible = ctx.solution().is_feasible()
        print("Instance:", progress)
        print("Args:")
        keys = list(args.keys())
        keys.sort()
        for key in keys:
            print(f"  {key}:", args[key])
        print("Time:", elapsed_time)
        print("Construction:", construction)
        print("Best:", value)
        print("Feasible:", feasible)
        print()

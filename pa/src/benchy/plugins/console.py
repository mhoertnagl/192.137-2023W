from abc import ABC

from benchy.testbench import *
from benchy.plugins.plugin import Plugin


class ConsoleLogPlugin(Plugin, ABC):
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
        print(f"Running Harness '{ctx.harness().name()}'")

    def harness_after(self, ctx: HarnessContext):
        print()
        print(f"Harness '{ctx.harness().name()}' completed")

    def instance_before(self, ctx: BeforeInstanceContext):
        print(ctx.instance().args())

    def instance_after(self, ctx: AfterInstanceContext):
        pass

from abc import ABC

from benchy import *
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
        pass

    def problem_after(self, ctx: ProblemContext):
        pass

    def harness_before(self, ctx: HarnessContext):
        pass

    def harness_after(self, ctx: HarnessContext):
        pass

    def instance_before(self, ctx: BeforeInstanceContext):
        pass

    def instance_after(self, ctx: AfterInstanceContext):
        pass
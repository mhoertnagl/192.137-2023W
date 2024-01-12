import os
from abc import ABC

from benchy.testbench import *
from benchy.plugins.plugin import Plugin


class SaveBestPlugin(Plugin, ABC):

    def __init__(self, out_dir: str):
        self._out_dir = out_dir

    def testbench_before(self, testbench: Testbench):
        pass

    def testbench_after(self, testbench: Testbench):
        pass

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
        problem_name = ctx.problem().name()
        run = ctx.run()
        solution = ctx.solution()
        value = solution.value()
        os.makedirs(self._out_dir, exist_ok=True)
        filename = os.path.join(self._out_dir, f"{problem_name}_{run}_{value}.txt")
        with open(filename, "w") as file:
            file.write(solution.to_file())



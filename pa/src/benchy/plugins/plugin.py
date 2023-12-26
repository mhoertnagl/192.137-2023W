from abc import ABC, abstractmethod
from benchy.testbench import *


class Plugin(ABC):

    @abstractmethod
    def testbench_before(self, testbench: Testbench):
        pass

    @abstractmethod
    def testbench_after(self, testbench: Testbench):
        pass

    @abstractmethod
    def problem_before(self, ctx: ProblemContext):
        pass

    @abstractmethod
    def problem_after(self, ctx: ProblemContext):
        pass

    @abstractmethod
    def harness_before(self, ctx: HarnessContext):
        pass

    @abstractmethod
    def harness_after(self, ctx: HarnessContext):
        pass

    @abstractmethod
    def instance_before(self, ctx: BeforeInstanceContext):
        pass

    @abstractmethod
    def instance_after(self, ctx: AfterInstanceContext):
        pass

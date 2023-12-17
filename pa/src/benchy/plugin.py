from abc import ABC, abstractmethod
from benchy import *


class Plugin(ABC):

    @abstractmethod
    def testbench_before(self,
                         testbench: Testbench):
        pass

    @abstractmethod
    def testbench_after(self,
                        testbench: Testbench):
        pass

    @abstractmethod
    def problem_before(self,
                       testbench: Testbench,
                       problem: Problem):
        pass

    @abstractmethod
    def problem_after(self,
                      testbench: Testbench,
                      problem: Problem):
        pass

    @abstractmethod
    def harness_before(self,
                       testbench: Testbench,
                       problem: Problem,
                       harness: Harness):
        pass

    @abstractmethod
    def harness_after(self,
                      testbench: Testbench,
                      problem: Problem,
                      harness: Harness):
        pass

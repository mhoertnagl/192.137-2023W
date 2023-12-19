from benchy import *


class ProblemContext:

    def __init__(self, testbench: Testbench, problem: IProblem):
        self._testbench = testbench
        self._problem = problem

    def testbench(self):
        return self._testbench

    def problem(self):
        return self._problem


class HarnessContext:

    def __init__(self, ctx: ProblemContext, harness: Harness):
        self._testbench = ctx.testbench
        self._problem = ctx.problem
        self._harness = harness

    def testbench(self):
        return self._testbench

    def problem(self):
        return self._problem

    def harness(self):
        return self._harness


class InstanceContext:

    def __init__(self, ctx: HarnessContext, instance: Instance):
        self._testbench = ctx.testbench
        self._problem = ctx.problem
        self._harness = ctx.harness
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
        self._testbench = ctx.testbench
        self._problem = ctx.problem
        self._harness = ctx.harness
        self._instance = ctx.instance
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
                 elapsed_time: float):
        self._testbench = ctx.testbench
        self._problem = ctx.problem
        self._harness = ctx.harness
        self._instance = ctx.instance
        self._run = run
        self._solution = solution
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

    def elapsed_time(self):
        return self._elapsed_time
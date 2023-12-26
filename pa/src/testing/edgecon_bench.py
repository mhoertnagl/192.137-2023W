from abc import ABC

from benchy import Testbench, Fixture, Harness
from benchy.plugins import ConsoleLogPlugin
from splex import read_file, Problem, Solution
from splex.con import EdgeConstruction

tb = Testbench()
log = ConsoleLogPlugin()

class EdgeConFixture(Fixture, ABC):

    def run(self, problem: Problem, args: dict[str, any]) -> Solution:
        con = EdgeConstruction(k=args["k"])
        return con.construct(problem)

if __name__ == '__main__':
    f1 = EdgeConFixture()
    h1 = Harness("Edge Construction", f1, 30)
    h1.add_parameter("k", [25, 50, 100])

    p1 = read_file("../../inst/testing/heur002_n_100_m_3274.txt")
    tb.add_plugin(log)
    tb.add_harness(h1)
    tb.add_problem(p1)
    tb.run()

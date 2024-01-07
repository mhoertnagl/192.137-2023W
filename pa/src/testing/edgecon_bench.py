from abc import ABC

from benchy import Testbench, Fixture, Harness
from benchy.plugins import ConsoleLogPlugin, CsvPlugin
from splex import read_file, Problem, Solution
from splex.con import EdgeConstruction, VertexConstruction


class EdgeConFixture(Fixture, ABC):

    def run(self, problem: Problem, args: dict[str, any]) -> (Solution, list[int, float]):
        con = EdgeConstruction(k=args["k"])
        sol = con.construct(problem)
        return sol, [sol.value()]


class VertexConFixture(Fixture, ABC):

    def run(self, problem: Problem, args: dict[str, any]) -> (Solution, list[int, float]):
        con = VertexConstruction()
        sol = con.construct(problem)
        return sol, [sol.value()]


if __name__ == '__main__':
    tb = Testbench()

    f1 = EdgeConFixture()
    h1 = Harness("Edge Construction", f1, 30)
    h1.add_parameter("k", [25, 50, 100])

    f2 = VertexConFixture()
    h2 = Harness("Vertex Construction", f2, 30)

    p1 = read_file("../../inst/testing/heur002_n_100_m_3274.txt")

    tb.add_plugin(ConsoleLogPlugin())
    tb.add_plugin(CsvPlugin("../../res"))
    tb.add_harness(h1)
    tb.add_harness(h2)
    tb.add_problem(p1)
    tb.run()

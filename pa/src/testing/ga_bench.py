from abc import ABC

from benchy import Testbench, Fixture, Harness
from benchy.plugins import ConsoleLogPlugin, CsvPlugin
from splex import read_file, Problem, Solution
from splex.con import EdgeConstruction
from splex.ga import GA
from splex.ga.comb import PickCombiner
from splex.ga.mut import VertexMoveMutation
from splex.ga.rep import BestReplacer, EliteReplacer
from splex.ga.sel import RankSelection, RouletteSelection, TournamentSelection


class GAFixture(Fixture, ABC):

    def run(self, problem: Problem, args: dict[str, any]) -> (Solution, list[int | float]):
        ga = GA(
            size=args["pop_size"],
            construction=args["construction"],
            selection=args["selection"],
            combiner=args["combiner"],
            mutator=args["mutator"],
            replacer=args["replacer"],
            iterations=args["iterations"]
        )
        return ga.run(problem)


if __name__ == '__main__':
    tb = Testbench()
    f1 = GAFixture()
    h1 = Harness("Genetic Algorithm", f1, 1)
    h1.add_parameter("pop_size", [10])
    h1.add_parameter("construction", [
        # EdgeConstruction(25),
        # EdgeConstruction(50),
        EdgeConstruction(100)
    ])
    h1.add_parameter("selection", [
        # RankSelection(0.25),
        RankSelection(0.50),
        # RankSelection(0.75),
        # RouletteSelection(0.25),
        RouletteSelection(0.50),
        # RouletteSelection(0.75),
        # TournamentSelection(0.25, 2),
        TournamentSelection(0.50, 2),
        # TournamentSelection(0.75, 2),
        # TournamentSelection(0.25, 4),
        TournamentSelection(0.50, 4),
        # TournamentSelection(0.75, 4)
    ])
    h1.add_parameter("combiner", [
        # PickCombiner(0.25),
        PickCombiner(0.50),
        # PickCombiner(0.75),
    ])
    h1.add_parameter("mutator", [
        VertexMoveMutation(fc=0.05, fv=0.05),
        # VertexMoveMutation(fc=0.05, fv=0.10),
        # VertexMoveMutation(fc=0.10, fv=0.05),
        # VertexMoveMutation(fc=0.10, fv=0.10),
        # VertexMoveMutation(fc=0.15, fv=0.05),
        VertexMoveMutation(fc=0.15, fv=0.10),
    ])
    h1.add_parameter("replacer", [
        BestReplacer(),
        # EliteReplacer(0.10),
        EliteReplacer(0.25),
        # EliteReplacer(0.50),
    ])
    # h1.add_parameter("iterations", [100, 500, 1000])
    h1.add_parameter("iterations", [250])

    p1 = read_file("../../inst/testing/heur002_n_100_m_3274.txt")
    # p1 = read_file("../../inst/testing/heur037_n_347_m_31752.txt")
    # p1 = read_file("../../inst/tuning/heur040_n_300_m_13358.txt")
    # p1 = read_file("../../inst/tuning/heur044_n_300_m_3234.txt")
    tb.add_plugin(ConsoleLogPlugin())
    tb.add_plugin(CsvPlugin("../../res"))
    tb.add_harness(h1)
    tb.add_problem(p1)
    tb.run()

from abc import ABC

from benchy import Testbench, Fixture, Harness
from benchy.plugins import ConsoleLogPlugin, CsvPlugin
from benchy.plugins.best import SaveBestPlugin
from splex import read_file, read_dir, Problem, Solution
from splex.con import EdgeConstruction, VertexConstruction, VertexConstruction2
from splex.ga import GA
from splex.ga.comb import PickCombiner, ConvergeCombiner, ConstructCombiner
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
    h1.add_parameter("pop_size", [25])
    h1.add_parameter("construction", [
        # EdgeConstruction(25),
        # EdgeConstruction(50),
        # EdgeConstruction(100)
        VertexConstruction()
    ])
    h1.add_parameter("selection", [
        # RankSelection(0.25),
        # RankSelection(0.50),
        # RankSelection(0.75),
        # RouletteSelection(0.25),
        # RouletteSelection(0.50),
        # RouletteSelection(0.75),
        # TournamentSelection(0.25, 2),
        TournamentSelection(0.50, 2),
        # TournamentSelection(0.75, 2),
        # TournamentSelection(0.25, 4),
        # TournamentSelection(0.50, 4),
        # TournamentSelection(0.75, 4)
    ])
    h1.add_parameter("combiner", [
        # PickCombiner(0.25),
        # PickCombiner(0.50),
        # PickCombiner(0.75),
        # ConvergeCombiner(0.50),
        ConstructCombiner(0.50)
    ])
    h1.add_parameter("mutator", [
        VertexMoveMutation(fc=0.05, fv=0.05),
        # VertexMoveMutation(fc=0.05, fv=0.25),
        # VertexMoveMutation(fc=0.25, fv=0.25),
        # VertexMoveMutation(fc=0.10, fv=0.10),
        # VertexMoveMutation(fc=0.50, fv=0.50),
        # VertexMoveMutation(fc=0.75, fv=0.75),
    ])
    h1.add_parameter("replacer", [
        BestReplacer(),
        # EliteReplacer(0.10),
        # EliteReplacer(0.25),
        # EliteReplacer(0.50),
    ])
    # h1.add_parameter("iterations", [100, 500, 1000])
    h1.add_parameter("iterations", [1000])

    p1 = read_file("../../inst/testing/heur002_n_100_m_3274.txt")
    # p1 = read_file("../../inst/testing/heur037_n_347_m_31752.txt")

    # p1 = read_file("../../inst/tuning/heur040_n_300_m_13358.txt")
    # p1 = read_file("../../inst/tuning/heur044_n_300_m_3234.txt")
    # p1 = read_file("../../inst/tuning/heur046_n_300_m_13150.txt")
    # p1 = read_file("../../inst/tuning/heur048_n_300_m_14666.txt")
    ## p1 = read_file("../../inst/tuning/heur053_n_300_m_39861.txt")
    # p1 = read_file("../../inst/tuning/heur055_n_300_m_5164.txt")

    p1 = read_file("../../inst/competition/heur049_n_300_m_17695.txt")
    # p1 = read_file("../../inst/competition/heur050_n_300_m_19207.txt")
    # p1 = read_file("../../inst/competition/heur051_n_300_m_20122.txt")

    # ps = read_dir("../../inst/tuning")

    tb.add_plugin(ConsoleLogPlugin())
    tb.add_plugin(CsvPlugin('../../res'))
    tb.add_plugin(SaveBestPlugin('../../res/solutions'))
    tb.add_harness(h1)
    tb.add_problem(p1)
    # tb.add_problems(ps)
    tb.run()

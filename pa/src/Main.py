#!/usr/bin/env python3
# -*- coding: utf8 -*-
from abc import ABC

import testbench as tb
from problem import Problem
from solution import Solution
import detcon as dc
import rancon as rc
import neighborhoods as nhs
import annealer
import grasper
import localsearch
import vnd
import termination


def main():
    # vnd_bench = tb.ParallelTestbench()
    # # vnd_bench.add_directory("../inst/testing")
    # # vnd_bench.add_directory("../inst/competition")
    # vnd_bench.add_benchmark(VndRandom134Benchmark())
    # vnd_bench.add_benchmark(VndRandom143Benchmark())
    # vnd_bench.add_benchmark(VndRandom314Benchmark())
    # vnd_bench.add_benchmark(VndRandom341Benchmark())
    # vnd_bench.run()

    # vnd_bench = tb.ParallelTestbench(n=5)
    # vnd_bench.add_directory("../inst/testing")
    # # vnd_bench.add_directory("../inst/competition")
    # vnd_bench.add_benchmark(VndBest1Benchmark())
    # vnd_bench.run()

    # sa_bench = tb.ParallelTestbench(n=5)
    # sa_bench.add_directory("../inst/testing")
    # sa_bench.add_directory("../inst/competition")
    # sa_bench.add_benchmark(SARandomUnionBenchmark())
    # sa_bench.add_benchmark(SAComponentMergeRandomBenchmark())
    # sa_bench.add_benchmark(SAComponentMergeRandomBenchmark())
    # sa_bench.add_benchmark(SAVertexMoveRandomBenchmark())
    # sa_bench.add_benchmark(SAVertexSwapRandomBenchmark())
    # sa_bench.add_benchmark(SATwoExchangeRandomBenchmark())
    # # sa_bench.add_benchmark(SATwoFlipRandomBenchmark())
    # # sa_bench.add_benchmark(SAFirstBenchmark())
    # sa_bench.run()

    # ls_bench = tb.ParallelTestbench(n=5)
    # ls_bench.add_directory("../inst/competition")
    # # ls_bench.add_directory("../inst/testing")
    # ls_bench.add_benchmark(LSRURBenchmark())
    # ls_bench.add_benchmark(LSVMRBenchmark())
    # ls_bench.add_benchmark(LSCMRBenchmark())
    # # ls_bench.add_benchmark(LSTFRBenchmark())
    # ls_bench.add_benchmark(LSVSRBenchmark())
    # ls_bench.add_benchmark(LSTERBenchmark())
    # ls_bench.run()
    #
    # ls_bench = tb.ParallelTestbench(n=5)
    # ls_bench.add_directory("../inst/competition")
    # # ls_bench.add_directory("../inst/testing")
    # ls_bench.add_benchmark(LSRUFBenchmark())
    # ls_bench.add_benchmark(LSVMFBenchmark())
    # ls_bench.add_benchmark(LSCMFBenchmark())
    # # ls_bench.add_benchmark(LSTFFBenchmark())
    # ls_bench.add_benchmark(LSVSFBenchmark())
    # ls_bench.add_benchmark(LSTEFBenchmark())
    # ls_bench.run()

    ls_bench = tb.ParallelTestbench(n=5)
    ls_bench.add_directory("../inst/competition")
    # ls_bench.add_directory("../inst/testing")
    ls_bench.add_benchmark(LSRUBBenchmark())
    ls_bench.add_benchmark(LSVMBBenchmark())
    ls_bench.add_benchmark(LSCMBBenchmark())
    # ls_bench.add_benchmark(LSTFBBenchmark())
    ls_bench.add_benchmark(LSVSBBenchmark())
    ls_bench.add_benchmark(LSTEBBenchmark())
    ls_bench.run()

    con_bench = tb.ParallelTestbench(n=1)
    # con_bench.add_directory("../inst/testing")
    # con_bench.add_directory("../inst/tuning")
    con_bench.add_directory("../inst/competition")
    # con_bench.add_benchmark(DetCon1Benchmark())
    # con_bench.add_benchmark(DetCon2Benchmark())
    # con_bench.add_benchmark(RanCon1Benchmark())
    con_bench.add_benchmark(GraspBenchmark())
    con_bench.run()


class LSRURBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(False)

    def name(self) -> str:
        return "LS RU R"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh1 = nhs.RandomUnionNeighborhood(nhs.Improvement.RANDOM)
        ls = localsearch.LocalSearch(nbh1, ter)
        sol = con.construct()
        return ls.run(sol)


class LSVMRBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(False)

    def name(self) -> str:
        return "LS VM R"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.RANDOM)
        ls = localsearch.LocalSearch(nbh1, ter)
        sol = con.construct()
        return ls.run(sol)


class LSVSRBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(False)

    def name(self) -> str:
        return "LS VS R"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh2 = nhs.VertexSwapNeighborhood(nhs.Improvement.RANDOM)
        ls = localsearch.LocalSearch(nbh2, ter)
        sol = con.construct()
        return ls.run(sol)


class LSCMRBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(False)

    def name(self) -> str:
        return "LS CM R"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh3 = nhs.ComponentMergeNeighborhood(nhs.Improvement.RANDOM)
        ls = localsearch.LocalSearch(nbh3, ter)
        sol = con.construct()
        return ls.run(sol)


class LSTFRBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(False)

    def name(self) -> str:
        return "LS TF R"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh4 = nhs.TwoFlipNeighborhood(nhs.Improvement.RANDOM)
        ls = localsearch.LocalSearch(nbh4, ter)
        sol = con.construct()
        return ls.run(sol)


class LSTERBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(False)

    def name(self) -> str:
        return "LS TE R"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh5 = nhs.TwoExchangeNeighborhood(nhs.Improvement.RANDOM)
        ls = localsearch.LocalSearch(nbh5, ter)
        sol = con.construct()
        return ls.run(sol)


class LSRUFBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(False)

    def name(self) -> str:
        return "LS RU F"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh1 = nhs.RandomUnionNeighborhood(nhs.Improvement.FIRST)
        ls = localsearch.LocalSearch(nbh1, ter)
        sol = con.construct()
        return ls.run(sol)


class LSVMFBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(True)

    def name(self) -> str:
        return "LS VM F"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.FIRST)
        ls = localsearch.LocalSearch(nbh1, ter)
        sol = con.construct()
        return ls.run(sol)


class LSVSFBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(True)

    def name(self) -> str:
        return "LS VS F"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh2 = nhs.VertexSwapNeighborhood(nhs.Improvement.FIRST)
        ls = localsearch.LocalSearch(nbh2, ter)
        sol = con.construct()
        return ls.run(sol)


class LSCMFBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(True)

    def name(self) -> str:
        return "LS CM F"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh3 = nhs.ComponentMergeNeighborhood(nhs.Improvement.FIRST)
        ls = localsearch.LocalSearch(nbh3, ter)
        sol = con.construct()
        return ls.run(sol)


class LSTFFBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(True)

    def name(self) -> str:
        return "LS TF F"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh4 = nhs.TwoFlipNeighborhood(nhs.Improvement.FIRST)
        ls = localsearch.LocalSearch(nbh4, ter)
        sol = con.construct()
        return ls.run(sol)


class LSTEFBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(True)

    def name(self) -> str:
        return "LS TE F"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh5 = nhs.TwoExchangeNeighborhood(nhs.Improvement.FIRST)
        ls = localsearch.LocalSearch(nbh5, ter)
        sol = con.construct()
        return ls.run(sol)


class LSRUBBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(False)

    def name(self) -> str:
        return "LS RU B"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh1 = nhs.RandomUnionNeighborhood(nhs.Improvement.BEST)
        ls = localsearch.LocalSearch(nbh1, ter)
        sol = con.construct()
        return ls.run(sol)


class LSVMBBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(True)

    def name(self) -> str:
        return "LS VM B"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.BEST)
        ls = localsearch.LocalSearch(nbh1, ter)
        sol = con.construct()
        return ls.run(sol)


class LSVSBBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(True)

    def name(self) -> str:
        return "LS VS B"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh2 = nhs.VertexSwapNeighborhood(nhs.Improvement.BEST)
        ls = localsearch.LocalSearch(nbh2, ter)
        sol = con.construct()
        return ls.run(sol)


class LSCMBBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(True)

    def name(self) -> str:
        return "LS CM B"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh3 = nhs.ComponentMergeNeighborhood(nhs.Improvement.BEST)
        ls = localsearch.LocalSearch(nbh3, ter)
        sol = con.construct()
        return ls.run(sol)


class LSTFBBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(True)

    def name(self) -> str:
        return "LS TF B"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh4 = nhs.TwoFlipNeighborhood(nhs.Improvement.BEST)
        ls = localsearch.LocalSearch(nbh4, ter)
        sol = con.construct()
        return ls.run(sol)


class LSTEBBenchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(True)

    def name(self) -> str:
        return "LS TE B"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        ter = termination.IterationTermination(1000)
        nbh5 = nhs.TwoExchangeNeighborhood(nhs.Improvement.BEST)
        ls = localsearch.LocalSearch(nbh5, ter)
        sol = con.construct()
        return ls.run(sol)


class DetCon1Benchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(True)

    def name(self) -> str:
        return "Deterministic Construction 1"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        return con.construct()


class DetCon2Benchmark(tb.Benchmark, ABC):

    def __init__(self):
        super().__init__(True)

    def name(self) -> str:
        return "Deterministic Construction 2"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon2(problem)
        return con.construct()


class RanCon1Benchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "Randomized Construction 1"

    def run(self, problem: Problem) -> Solution:
        con = rc.RanCon1(problem)
        return con.construct()


class GraspBenchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "GRASP"

    def run(self, problem: Problem) -> Solution:
        con = rc.RanCon1(problem)
        nbh = nhs.RandomUnionNeighborhood(nhs.Improvement.FIRST)
        ls_ter = termination.IterationTermination(7500)
        # ls_ter = termination.ImprovementTermination(1)
        ls = localsearch.LocalSearch(nbh, ls_ter)
        gr_ter = termination.IterationTermination(750)
        # gr_ter = termination.ImprovementTermination(1)
        grasp = grasper.Grasper(con, ls, gr_ter)
        return grasp.run()


class VndRandom134Benchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "VND Random 135"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.BEST)
        # nbh2 = nhs.VertexSwapNeighborhood(nhs.Improvement.BEST)
        nbh3 = nhs.ComponentMergeNeighborhood(nhs.Improvement.BEST)
        # nbh4 = nhs.TwoFlipNeighborhood(nhs.Improvement.BEST)
        nbh5 = nhs.TwoExchangeNeighborhood(nhs.Improvement.BEST)
        vn = vnd.VND([nbh1, nbh3, nbh5])
        sol = con.construct()
        return vn.run(sol)


class VndRandom143Benchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "VND Random 153"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.BEST)
        # nbh2 = nhs.VertexSwapNeighborhood(nhs.Improvement.BEST)
        nbh3 = nhs.ComponentMergeNeighborhood(nhs.Improvement.BEST)
        # nbh4 = nhs.TwoFlipNeighborhood(nhs.Improvement.BEST)
        nbh5 = nhs.TwoExchangeNeighborhood(nhs.Improvement.BEST)
        vn = vnd.VND([nbh1, nbh5, nbh3])
        sol = con.construct()
        return vn.run(sol)


class VndRandom314Benchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "VND Random 315"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.BEST)
        # nbh2 = nhs.VertexSwapNeighborhood(nhs.Improvement.BEST)
        nbh3 = nhs.ComponentMergeNeighborhood(nhs.Improvement.BEST)
        # nbh4 = nhs.TwoFlipNeighborhood(nhs.Improvement.BEST)
        nbh5 = nhs.TwoExchangeNeighborhood(nhs.Improvement.BEST)
        vn = vnd.VND([nbh3, nbh1, nbh5])
        sol = con.construct()
        return vn.run(sol)


class VndRandom341Benchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "VND Random 351"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.BEST)
        # nbh2 = nhs.VertexSwapNeighborhood(nhs.Improvement.BEST)
        nbh3 = nhs.ComponentMergeNeighborhood(nhs.Improvement.BEST)
        nbh4 = nhs.TwoFlipNeighborhood(nhs.Improvement.BEST)
        nbh5 = nhs.TwoExchangeNeighborhood(nhs.Improvement.BEST)
        vn = vnd.VND([nbh3, nbh5, nbh1])
        sol = con.construct()
        return vn.run(sol)


class SARandomUnionBenchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "SA random union Random"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.RandomUnionNeighborhood(nhs.Improvement.RANDOM)
        ter = termination.IterationTermination(100)
        sol = con.construct()
        sa = annealer.Annealer(sol, nbh1, ter)
        return sa.run()


class SATwoFlipRandomBenchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "SA 2-flip Random"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.TwoFlipNeighborhood(nhs.Improvement.RANDOM)
        ter = termination.IterationTermination(100)
        sol = con.construct()
        sa = annealer.Annealer(sol, nbh1, ter)
        return sa.run()


class SATwoExchangeRandomBenchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "SA 2-exchange Random"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.TwoExchangeNeighborhood(nhs.Improvement.RANDOM)
        ter = termination.IterationTermination(100)
        sol = con.construct()
        sa = annealer.Annealer(sol, nbh1, ter)
        return sa.run()


class SAComponentMergeRandomBenchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "SA component merge Random"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.ComponentMergeNeighborhood(nhs.Improvement.RANDOM)
        ter = termination.IterationTermination(100)
        sol = con.construct()
        sa = annealer.Annealer(sol, nbh1, ter)
        return sa.run()


class SAVertexSwapRandomBenchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "SA vertex swap Random"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexSwapNeighborhood(nhs.Improvement.RANDOM)
        ter = termination.IterationTermination(100)
        sol = con.construct()
        sa = annealer.Annealer(sol, nbh1, ter)
        return sa.run()


class SAVertexMoveRandomBenchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "SA vertex move Random"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.RANDOM)
        ter = termination.IterationTermination(100)
        sol = con.construct()
        sa = annealer.Annealer(sol, nbh1, ter)
        return sa.run()


class SAFirstBenchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "SA First 10"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.FIRST)
        ter = termination.IterationTermination(10)
        sol = con.construct()
        sa = annealer.Annealer(sol, nbh1, ter)
        return sa.run()


if __name__ == '__main__':
    main()

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
    # con_bench = tb.ParallelTestbench()
    # con_bench.add_directory("../inst/competition")
    # con_bench.add_benchmark(DetCon1Benchmark())
    # con_bench.add_benchmark(DetCon2Benchmark())
    # con_bench.add_benchmark(RanCon1Benchmark())
    # con_bench.add_benchmark(GraspBenchmark())
    # con_bench.run()

    vnd_bench = tb.ParallelTestbench()
    vnd_bench.add_directory("../inst/competition")
    vnd_bench.add_benchmark(VndRandom134Benchmark())
    vnd_bench.add_benchmark(VndRandom143Benchmark())
    # vnd_bench.add_benchmark(VndRandom314Benchmark())
    # vnd_bench.add_benchmark(VndRandom341Benchmark())
    vnd_bench.run()


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
        nbh = nhs.VertexMoveNeighborhood(nhs.Improvement.RANDOM)
        ls_ter = termination.IterationTermination(100)
        # ls_ter = termination.ImprovementTermination(1)
        ls = localsearch.LocalSearch(nbh, ls_ter)
        gr_ter = termination.IterationTermination(10)
        # gr_ter = termination.ImprovementTermination(1)
        grasp = grasper.Grasper(con, ls, gr_ter)
        return grasp.run()


class VndRandom134Benchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "VND Random 134"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.RANDOM)
        # nbh2 = nhs.VertexSwapNeighborhood(nhs.Improvement.RANDOM)
        nbh3 = nhs.ComponentMergeNeighborhood(nhs.Improvement.RANDOM)
        nbh4 = nhs.TwoFlipNeighborhood(nhs.Improvement.RANDOM)
        # nbh5 = nhs.TwoExchangeNeighborhood(nhs.Improvement.RANDOM)
        vn = vnd.VND([nbh1, nbh3, nbh4])
        sol = con.construct()
        return vn.run(sol)


class VndRandom143Benchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "VND Random 143"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.RANDOM)
        # nbh2 = nhs.VertexSwapNeighborhood(nhs.Improvement.RANDOM)
        nbh3 = nhs.ComponentMergeNeighborhood(nhs.Improvement.RANDOM)
        nbh4 = nhs.TwoFlipNeighborhood(nhs.Improvement.RANDOM)
        # nbh5 = nhs.TwoExchangeNeighborhood(nhs.Improvement.RANDOM)
        vn = vnd.VND([nbh1, nbh4, nbh3])
        sol = con.construct()
        return vn.run(sol)


class VndRandom314Benchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "VND Random 314"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.RANDOM)
        # nbh2 = nhs.VertexSwapNeighborhood(nhs.Improvement.RANDOM)
        nbh3 = nhs.ComponentMergeNeighborhood(nhs.Improvement.RANDOM)
        nbh4 = nhs.TwoFlipNeighborhood(nhs.Improvement.RANDOM)
        # nbh5 = nhs.TwoExchangeNeighborhood(nhs.Improvement.RANDOM)
        vn = vnd.VND([nbh3, nbh1, nbh4])
        sol = con.construct()
        return vn.run(sol)


class VndRandom341Benchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "VND Random 341"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.RANDOM)
        # nbh2 = nhs.VertexSwapNeighborhood(nhs.Improvement.RANDOM)
        nbh3 = nhs.ComponentMergeNeighborhood(nhs.Improvement.RANDOM)
        nbh4 = nhs.TwoFlipNeighborhood(nhs.Improvement.RANDOM)
        # nbh5 = nhs.TwoExchangeNeighborhood(nhs.Improvement.RANDOM)
        vn = vnd.VND([nbh3, nbh4, nbh1])
        sol = con.construct()
        return vn.run(sol)


if __name__ == '__main__':
    main()

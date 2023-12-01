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
    con_bench = tb.ParallelTestbench(n=5)
    # con_bench.add_directory("../inst/testing")
    # con_bench.add_directory("../inst/tuning")
    # con_bench.add_directory("../inst/competition")
    con_bench.add_filename("../inst/tuning/heur042_n_300_m_5764.txt")
    con_bench.add_filename("../inst/tuning/heur044_n_300_m_3234.txt")
    con_bench.add_filename("../inst/tuning/heur046_n_300_m_13150.txt")
    con_bench.add_filename("../inst/tuning/heur056_n_300_m_12131.txt")
    con_bench.add_filename("../inst/tuning/heur059_n_300_m_7867.txt")
    con_bench.add_benchmark(DetCon1Benchmark())
    con_bench.add_benchmark(DetCon2Benchmark())
    con_bench.add_benchmark(RanCon1Benchmark())
    # con_bench.add_benchmark(GraspRandomBenchmark())
    # con_bench.add_benchmark(GraspFirstBenchmark())
    con_bench.add_benchmark(GraspBestBenchmark())
    con_bench.run()


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


class GraspRandomBenchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "GRASP"

    def run(self, problem: Problem) -> Solution:
        con = rc.RanCon1(problem, 15)
        nbh = nhs.RandomUnionNeighborhood(nhs.Improvement.RANDOM)
        ls_ter = termination.IterationTermination(100)
        # ls_ter = termination.ImprovementTermination(1)
        ls = localsearch.LocalSearch(nbh, ls_ter)
        gr_ter = termination.IterationTermination(10)
        # gr_ter = termination.ImprovementTermination(1)
        grasp = grasper.Grasper(con, ls, gr_ter)
        return grasp.run()


class GraspFirstBenchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "GRASP"

    def run(self, problem: Problem) -> Solution:
        con = rc.RanCon1(problem, 15)
        nbh = nhs.RandomUnionNeighborhood(nhs.Improvement.FIRST)
        ls_ter = termination.IterationTermination(100)
        # ls_ter = termination.ImprovementTermination(1)
        ls = localsearch.LocalSearch(nbh, ls_ter)
        gr_ter = termination.IterationTermination(10)
        # gr_ter = termination.ImprovementTermination(1)
        grasp = grasper.Grasper(con, ls, gr_ter)
        return grasp.run()


class GraspBestBenchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "GRASP"

    def run(self, problem: Problem) -> Solution:
        con = rc.RanCon1(problem, 15)
        nbh = nhs.RandomUnionNeighborhood(nhs.Improvement.BEST)
        ls_ter = termination.IterationTermination(10)
        # ls_ter = termination.ImprovementTermination(1)
        ls = localsearch.LocalSearch(nbh, ls_ter)
        gr_ter = termination.IterationTermination(100)
        # gr_ter = termination.ImprovementTermination(1)
        grasp = grasper.Grasper(con, ls, gr_ter)
        return grasp.run()


if __name__ == '__main__':
    main()

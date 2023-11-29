#!/usr/bin/env python3
# -*- coding: utf8 -*-
from abc import ABC

import grasper
import localsearch
import termination
from problem import Problem
from reader import Reader
import detcon as dc
import rancon as rc
import neighborhoods as nhs
from annealer import Annealer
from localsearch import LocalSearch
from grasper import Grasper
from solution import Solution
from vnd import VND
import testbench as tb


def main():
    con_bench = tb.ParallelTestbench()
    # con_bench.add_filename("../inst/testing/test.txt")
    # con_bench.add_filename("../inst/testing/heur002_n_100_m_3274.txt")
    # con_bench.add_filename("../inst/testing/heur003_n_120_m_2588.txt")
    # con_bench.add_filename("../inst/testing/heur004_n_140_m_3014.txt")
    # con_bench.add_filename("../inst/testing/heur005_n_160_m_4015.txt")
    con_bench.add_directory("../inst/competition")
    con_bench.add_benchmark(DetCon1Benchmark())
    con_bench.add_benchmark(DetCon2Benchmark())
    con_bench.add_benchmark(RanCon1Benchmark())
    con_bench.add_benchmark(GraspBenchmark())
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


if __name__ == '__main__':
    main()

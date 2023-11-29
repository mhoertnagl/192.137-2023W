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
    con_bench = tb.Testbench()
    con_bench.add_filename("../inst/testing/test.txt")
    con_bench.add_filename("../inst/testing/heur002_n_100_m_3274.txt")
    # con_bench.add_filename("../inst/testing/heur003_n_120_m_2588.txt")
    # con_bench.add_filename("../inst/testing/heur004_n_140_m_3014.txt")
    # con_bench.add_filename("../inst/testing/heur005_n_160_m_4015.txt")
    con_bench.add_benchmark(DetCon1Benchmark())
    con_bench.add_benchmark(DetCon2Benchmark())
    con_bench.add_benchmark(RanCon1Benchmark())
    con_bench.add_benchmark(GraspBenchmark())
    con_bench.run()


class DetCon1Benchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "Deterministic Construction 1"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        return con.construct()


class DetCon2Benchmark(tb.Benchmark, ABC):

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
        ls = localsearch.LocalSearch(nbh, ls_ter)
        gr_ter = termination.IterationTermination(10)
        grasp = grasper.Grasper(con, ls, gr_ter)
        return grasp.run()


if __name__ == '__main__':
    main()

    # reader = Reader()
    #
    # problem = reader.read("../inst/testing/test.txt")
    # # problem = reader.read("../inst/testing/heur002_n_100_m_3274.txt")
    # # problem = reader.read("../inst/testing/heur003_n_120_m_2588.txt")
    # # problem = reader.read("../inst/testing/heur004_n_140_m_3014.txt")
    # # problem = reader.read("../inst/testing/heur005_n_160_m_4015.txt")
    # print(problem)
    #
    # # con = dc.DetCon3(problem)
    # con = dc.DetCon2(problem)
    # # con = dc.DetCon1(problem)
    # # con = rc.RanCon1(problem, 10)
    # sol = con.construct()
    # print(sol.is_feasible())
    # sol.draw()
    # print(sol.get_value())
    #
    # # nbh = nhs.ComponentMergeNeighborhood(10)
    # # ls = LocalSearch(nbh, 1000)
    # # sol = ls.run(sol)
    # # print(sol.is_feasible())
    # # sol.draw()
    # # print(sol.get_value())
    #
    # nbh = nhs.TwoFlipNeighborhood(nhs.Improvement.RANDOM)
    # ter = termination.IterationTermination(1000)
    # ls = LocalSearch(nbh, ter)
    # sol = ls.run(sol)
    # print(sol.is_feasible())
    # sol.draw()
    # print(sol.get_value())
    #
    # # nbh1 = nhs.VertexSwapNeighborhood()
    # # ls1 = LocalSearch(nbh1, 1000)
    # # sol1 = ls1.run(sol)
    # # # an = Annealer(sol, nbh1, 50, 0.75)
    # # # sol1 = an.run()
    # # print(sol1.is_feasible())
    # # sol1.draw()
    # # print(sol1.get_value())
    # #
    # # nbh2 = nhs.SingleComponentMultiExchangeNeighborhood()
    # # ls2 = LocalSearch(nbh2, 1000)
    # # sol2 = ls2.run(sol1)
    # # print(sol2.is_feasible())
    # # sol2.draw()
    # # print(sol2.get_value())
    #
    # # nbh = nhs.VertexMoveNeighborhood()
    # # ls = LocalSearch(nbh, 1000)
    # # con = rc.RanCon1(problem, 10)
    # # gsp = Grasper(ls, con, 100)
    # # sol = gsp.run()
    # # print(sol.is_feasible())
    # # sol.draw()
    # # print(sol.get_value())
    #
    # # nbh1 = nhs.ComponentMergeNeighborhood()
    # # nbh2 = nhs.VertexMoveNeighborhood()
    # # nbh3 = nhs.TwoExchangeNeighborhood()
    # # vnd = VND([nbh1, nbh2, nbh3])
    # # con = dc.DetCon2(problem)
    # # sol = con.construct()
    # # sol = vnd.run(sol)
    # # print(sol.is_feasible())
    # # sol.draw()
    # # print(sol.get_value())

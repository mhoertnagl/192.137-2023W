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
    sa_bench = tb.ParallelTestbench(n=5)
    sa_bench.add_directory("../inst/testing")
    sa_bench.add_directory("../inst/competition")
    # sa_bench.add_benchmark(SARandomUnionBenchmark())
    sa_bench.add_benchmark(SAComponentMergeRandomBenchmark())
    sa_bench.add_benchmark(SAVertexMoveRandomBenchmark())
    # sa_bench.add_benchmark(SAVertexSwapRandomBenchmark())
    sa_bench.add_benchmark(SATwoExchangeRandomBenchmark())
    # sa_bench.add_benchmark(SATwoFlipRandomBenchmark())
    # sa_bench.add_benchmark(SAFirstBenchmark())
    sa_bench.run()


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


class SATwoExchangeRandomBenchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "SA TE"

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


# class SARandomUnionBenchmark(tb.Benchmark, ABC):
#
#     def name(self) -> str:
#         return "SA random union Random"
#
#     def run(self, problem: Problem) -> Solution:
#         con = dc.DetCon1(problem)
#         nbh1 = nhs.RandomUnionNeighborhood(nhs.Improvement.RANDOM)
#         ter = termination.IterationTermination(100)
#         sol = con.construct()
#         sa = annealer.Annealer(sol, nbh1, ter)
#         return sa.run()
#
#
# class SATwoFlipRandomBenchmark(tb.Benchmark, ABC):
#
#     def name(self) -> str:
#         return "SA 2-flip Random"
#
#     def run(self, problem: Problem) -> Solution:
#         con = dc.DetCon1(problem)
#         nbh1 = nhs.TwoFlipNeighborhood(nhs.Improvement.RANDOM)
#         ter = termination.IterationTermination(100)
#         sol = con.construct()
#         sa = annealer.Annealer(sol, nbh1, ter)
#         return sa.run()
#
#
# class SAVertexSwapRandomBenchmark(tb.Benchmark, ABC):
#
#     def name(self) -> str:
#         return "SA vertex swap Random"
#
#     def run(self, problem: Problem) -> Solution:
#         con = dc.DetCon1(problem)
#         nbh1 = nhs.VertexSwapNeighborhood(nhs.Improvement.RANDOM)
#         ter = termination.IterationTermination(100)
#         sol = con.construct()
#         sa = annealer.Annealer(sol, nbh1, ter)
#         return sa.run()
#
#
#
# class SAFirstBenchmark(tb.Benchmark, ABC):
#
#     def name(self) -> str:
#         return "SA First 10"
#
#     def run(self, problem: Problem) -> Solution:
#         con = dc.DetCon1(problem)
#         nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.FIRST)
#         ter = termination.IterationTermination(10)
#         sol = con.construct()
#         sa = annealer.Annealer(sol, nbh1, ter)
#         return sa.run()


if __name__ == '__main__':
    main()

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
    vnd_bench = tb.ParallelTestbench()
    vnd_bench.add_filename("../inst/tuning/heur042_n_300_m_5764.txt")
    vnd_bench.add_filename("../inst/tuning/heur044_n_300_m_3234.txt")
    vnd_bench.add_filename("../inst/tuning/heur046_n_300_m_13150.txt")
    vnd_bench.add_filename("../inst/tuning/heur056_n_300_m_12131.txt")
    vnd_bench.add_filename("../inst/tuning/heur059_n_300_m_7867.txt")
    # vnd_bench.add_directory("../inst/testing")
    # vnd_bench.add_directory("../inst/competition")
    vnd_bench.add_benchmark(Vnd123Benchmark())
    vnd_bench.add_benchmark(Vnd132Benchmark())
    vnd_bench.add_benchmark(Vnd213Benchmark())
    vnd_bench.add_benchmark(Vnd231Benchmark())
    vnd_bench.add_benchmark(Vnd312Benchmark())
    vnd_bench.add_benchmark(Vnd321Benchmark())
    vnd_bench.run()


class Vnd123Benchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "VND 123"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.BEST)
        nbh2 = nhs.ComponentMergeNeighborhood(nhs.Improvement.BEST)
        nbh3 = nhs.TwoExchangeNeighborhood(nhs.Improvement.BEST)
        vn = vnd.VND([nbh1, nbh2, nbh3])
        sol = con.construct()
        return vn.run(sol)


class Vnd132Benchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "VND 132"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.BEST)
        nbh2 = nhs.ComponentMergeNeighborhood(nhs.Improvement.BEST)
        nbh3 = nhs.TwoExchangeNeighborhood(nhs.Improvement.BEST)
        vn = vnd.VND([nbh1, nbh3, nbh2])
        sol = con.construct()
        return vn.run(sol)


class Vnd213Benchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "VND 213"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.BEST)
        nbh2 = nhs.ComponentMergeNeighborhood(nhs.Improvement.BEST)
        nbh3 = nhs.TwoExchangeNeighborhood(nhs.Improvement.BEST)
        vn = vnd.VND([nbh2, nbh1, nbh3])
        sol = con.construct()
        return vn.run(sol)


class Vnd231Benchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "VND 231"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.BEST)
        nbh2 = nhs.ComponentMergeNeighborhood(nhs.Improvement.BEST)
        nbh3 = nhs.TwoExchangeNeighborhood(nhs.Improvement.BEST)
        vn = vnd.VND([nbh2, nbh3, nbh1])
        sol = con.construct()
        return vn.run(sol)


class Vnd312Benchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "VND 312"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.BEST)
        nbh2 = nhs.ComponentMergeNeighborhood(nhs.Improvement.BEST)
        nbh3 = nhs.TwoExchangeNeighborhood(nhs.Improvement.BEST)
        vn = vnd.VND([nbh3, nbh1, nbh2])
        sol = con.construct()
        return vn.run(sol)


class Vnd321Benchmark(tb.Benchmark, ABC):

    def name(self) -> str:
        return "VND 321"

    def run(self, problem: Problem) -> Solution:
        con = dc.DetCon1(problem)
        nbh1 = nhs.VertexMoveNeighborhood(nhs.Improvement.BEST)
        nbh2 = nhs.ComponentMergeNeighborhood(nhs.Improvement.BEST)
        nbh3 = nhs.TwoExchangeNeighborhood(nhs.Improvement.BEST)
        vn = vnd.VND([nbh3, nbh2, nbh1])
        sol = con.construct()
        return vn.run(sol)


if __name__ == '__main__':
    main()

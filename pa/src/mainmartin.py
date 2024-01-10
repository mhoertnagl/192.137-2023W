# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 18:23:04 2023

@author: Martin
"""


import sys
import traceback
import argparse
import time

from reader import Reader
from detcon import DetCon1, DetCon2

import numpy as np
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
from grasper import Grasper
import matplotlib.pyplot as plt


reader = Reader()
problem = reader.read("../inst/testing/heur002_n_100_m_3274.txt")
# problem = reader.read("../inst//tuning/heur040_n_300_m_13358.txt")
# problem = reader.read("../inst/tuning/heur045_n_300_m_6293.txt")
# problem = reader.read("../inst/tuning/tuning/heur055_n_300_m_5164.txt")
# problem = reader.read("../inst/testing/test.txt")


problem.draw()

con = DetCon1(problem)
con = DetCon2(problem)
# # ran_con = rc.RanCon1(problem,3)
# con = dc.DetCon2(problem)
# # con = rc.RanCon1(problem)
sol = con.construct()
sol.draw()
print(sol.get_value())
print(sol.get_components())

# ls_ter = termination.IterationTermination(3,)

# # nbh = nhs.OneFlipNeighborhood(nhs.Improvement.FIRST)
# # ls = localsearch.LocalSearch(nbh, ls_ter)
# # sol = ls.run(sol)
# # print(sol.get_value())
# # print(sol.get_components())
# # sol.draw()

# improvements = [nhs.Improvement.FIRST,nhs.Improvement.BEST,nhs.Improvement.RANDOM]


# legends = ['Vertex Move',"Component Merge","Two Exchange","Two Flip"]
# lo_list = []
# f_list = []
# constructed_sol = con.construct()


# class LocalSearchBenchmark(tb.Benchmark, ABC):

#     def __init__(self):
#         super().__init__(True)    
        
#     def name(self) -> str:
#         return "LocalSearch"
    
#     def run(self, problem: Problem) -> Solution:
#         con = DetCon2(problem)
#         nbh = nhs.VertexMoveNeighborhood(nhs.Improvement.FIRST)
#         ls_ter = termination.IterationTermination(1000)
#         # ls_ter = termination.ImprovementTermination(1)
#         ls = localsearch.LocalSearch(nbh, ls_ter)
#         sol = con.construct()
#         return ls.run(sol)
    
    
# ls_bench = tb.ParallelTestbench(n=1)
# # con_bench.add_directory("../inst/testing")
# # ls_bench.add_directory("../inst/competition")
# # ls_bench.add_directory("../inst/tuning")
# ls_bench.add_filename("../inst/testing/heur001_n_10_m_31.txt")
# ls_bench.add_benchmark(LocalSearchBenchmark())
# ls_bench.run()




# improv=improvements[0]
# nbhs = [nhs.VertexMoveNeighborhood(improv),nhs.ComponentMergeNeighborhood(improv),nhs.TwoExchangeNeighborhood(improv),nhs.TwoFlipNeighborhood(improv)]
# index=3
# nbh = nbhs[index]
# sol = constructed_sol.copy()
# ls = localsearch.LocalSearchTuning(nbh, ls_ter)
# sol,c,f,lo = ls.run(sol)
# lo_list.append(lo)
# plt.plot(np.arange(0,len(f)),f,label = legends[index])

# plt.savefig("..//res/plots/heuOpt.png")

# for improv in improvements:
#     nbhs = [nhs.VertexMoveNeighborhood(improv),nhs.ComponentMergeNeighborhood(improv),nhs.ComponentMergeNeighborhood(improv)]
#     for index,nbh in enumerate(nbhs):    
#         # improv = improvements[0]
#         # nbh = nbhs[1]
#         sol = constructed_sol.copy()
#         ls = localsearch.LocalSearchTuning(nbh, ls_ter)
#         sol,c,f,lo = ls.run(sol)
#         lo_list.append(lo)
#         f_list.append(f)
#         plt.plot(np.arange(0,len(f)),f,label = legends[index])
#         # break
#     plt.legend()
#     plt.show()
#     # break




# nbh = nhs.ComponentMergeNeighborhood(nhs.Improvement.FIRST)
# ls = localsearch.LocalSearch(nbh, ls_ter)
# sol = ls.run(sol)
# print(sol.get_value())
# print(sol.get_components())
# sol.draw()

# nbh = nhs.OneFlipNeighborhood(nhs.Improvement.FIRST)
# ls = localsearch.LocalSearch(nbh, ls_ter)
# sol = ls.run(sol)
# print(sol.get_value())
# print(sol.get_components())
# sol.draw()

# ran_con = rc.RanCon1(problem,3)
# ls = localsearch.LocalSearch(nbh, ls_ter)
# grasp = Grasper(rc=ran_con,ls=ls,ter=ls_ter)
# sol = grasp.run()
# print(sol.get_value())
# print(sol.get_components())
# sol.draw()

# nbh = nhs.TwoExchangeNeighborhood(nhs.Improvement.BEST)
# ls = localsearch.LocalSearch(nbh, ls_ter)
# sol = ls.run(sol)
# sol.draw()
# print(sol.get_value())
# print(sol.get_components())









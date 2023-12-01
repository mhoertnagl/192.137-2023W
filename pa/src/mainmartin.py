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
# problem = reader.read("../inst/testing/heur002_n_100_m_3274.txt")
problem = reader.read("../inst//tuning/heur040_n_300_m_13358.txt")
# problem = reader.read("../inst/tuning/heur045_n_300_m_6293.txt")
# problem = reader.read("../inst/tuning/tuning/heur055_n_300_m_5164.txt")
# problem = reader.read("../inst/testing/test.txt")


problem.draw()

#con = DetCon1(problem)
ran_con = rc.RanCon1(problem,3)
con = dc.DetCon2(problem)
# con = rc.RanCon1(problem)
sol = con.construct()
sol.draw()
print(sol.get_value())
print(sol.get_components())

ls_ter = termination.IterationTermination(300,)

# nbh = nhs.OneFlipNeighborhood(nhs.Improvement.FIRST)
# ls = localsearch.LocalSearch(nbh, ls_ter)
# sol = ls.run(sol)
# print(sol.get_value())
# print(sol.get_components())
# sol.draw()

improvements = [nhs.Improvement.FIRST,nhs.Improvement.BEST,nhs.Improvement.RANDOM]



legends = ['Vertex Move',"Component Merge","Two Exchange"]
lo_list = []
f_list = []
constructed_sol = con.construct()

improv=improvements[1]
nbhs = [nhs.VertexMoveNeighborhood(improv),nhs.ComponentMergeNeighborhood(improv),nhs.TwoExchangeNeighborhood(improv)]
index=2
nbh = nbhs[1]
sol = constructed_sol.copy()
ls = localsearch.LocalSearchTuning(nbh, ls_ter)
sol,c,f,lo = ls.run(sol)
lo_list.append(lo)
plt.plot(np.arange(0,len(f)),f,label = legends[index])

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









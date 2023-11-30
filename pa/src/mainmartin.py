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

reader = Reader()
problem = reader.read("../inst/testing/heur002_n_100_m_3274.txt")
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

ls_ter = termination.IterationAndImprovementTermination(10)

# nbh = nhs.OneFlipNeighborhood(nhs.Improvement.FIRST)
# ls = localsearch.LocalSearch(nbh, ls_ter)
# sol = ls.run(sol)
# print(sol.get_value())
# print(sol.get_components())
# sol.draw()

nbh = nhs.VertexMoveNeighborhood(nhs.Improvement.FIRST)
# nbh = nhs.ComponentMergeNeighborhood(nhs.Improvement.BEST)
ls = localsearch.LocalSearch(nbh, ls_ter)
sol = ls.run(sol)
sol.draw()
print(sol.get_value())
print(sol.get_components())

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

ran_con = rc.RanCon1(problem,3)
ls = localsearch.LocalSearch(nbh, ls_ter)
grasp = Grasper(rc=ran_con,ls=ls,ter=ls_ter)
sol = grasp.run()
print(sol.get_value())
print(sol.get_components())
sol.draw()




# nbh = nhs.TwoExchangeNeighborhood(nhs.Improvement.BEST)
# ls = localsearch.LocalSearch(nbh, ls_ter)
# sol = ls.run(sol)
# sol.draw()
# print(sol.get_value())
# print(sol.get_components())



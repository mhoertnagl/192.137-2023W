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
from rancon import RanCon

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

reader = Reader()
problem = reader.read("../inst/testing/heur002_n_100_m_3274.txt")
problem.draw()

#con = DetCon1(problem)
#ran_con = RanCon(problem, 3)
con = DetCon2(problem)
sol = con.construct()
sol.draw()
print(sol.get_value())
print(sol.get_components())


nbh = nhs.VertexMoveNeighborhood(nhs.Improvement.FIRST)
ls_ter = termination.IterationTermination(10)
# ls_ter = termination.ImprovementTermination(1)
ls = localsearch.LocalSearch(nbh, ls_ter)
sol = ls.run(sol)
sol.draw()
print(sol.get_value())
print(sol.get_components())




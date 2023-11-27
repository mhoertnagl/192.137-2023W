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

reader = Reader()
problem = reader.read('test.txt')

problem.draw()

con = DetCon1(problem)
ran_con = RanCon(problem, 3)
# con = DetCon2(problem)
ran_solution = ran_con.construct()
ran_solution.draw()
print(ran_solution.evaluate())
print(ran_solution.components)


solution = con.construct()
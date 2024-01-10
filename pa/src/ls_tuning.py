# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 13:23:10 2023

@author: mfischer
"""

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
import os

reader = Reader()

# problem = reader.read("../inst/testing/heur002_n_100_m_3274.txt")

# inst_names = ["heur040_n_300_m_13358","heur045_n_300_m_6293","heur055_n_300_m_5164"]
inst_names = os.listdir("../inst/competition/")
# for x in os.listdir("../inst/testing/"):
    # inst_names.append(x) 
    
lo_list = []
f_list = []

for inst_name in inst_names:
    # problem = reader.read("../inst//tuning/"+inst_name+".txt")
    problem = reader.read("../inst/testing/heur002_n_100_m_3274.txt")
    con = dc.DetCon2(problem)
    
    ls_ter = termination.IterationAndImprovementTermination(1000)
    
    # improvements = [nhs.Improvement.FIRST,nhs.Improvement.BEST,nhs.Improvement.RANDOM]
    improvements = [nhs.Improvement.FIRST]

    # improv_names = ["First improvement","Best Improvement","Random"]
    improv_names = ["First improvement"]

    legends = ['Vertex Move',"Component Merge","Two Exchange"]
    lo_list = []
    f_list = []
    constructed_sol = con.construct()
    
    print('starting with',inst_name)
    
    fig, ax = plt.subplots(1,3)
    plt.figure(figsize=(20, 6))
    plt.suptitle(inst_name)
    for index2,improv in enumerate(improvements):
        # nbhs = [nhs.VertexMoveNeighborhood(improv),nhs.ComponentMergeNeighborhood(improv),nhs.ComponentMergeNeighborhood(improv)]
        nbhs = [nhs.VertexMoveNeighborhood(improv)]
        plt.subplot(131+index2)
        print(improv_names[index2])
        for index,nbh in enumerate(nbhs):    
            # improv = improvements[0]
            # nbh = nbhs[1]
            sol = constructed_sol.copy()
            ls = localsearch.LocalSearchTuning(nbh, ls_ter)
            sol,c,f,lo = ls.run(sol)
            lo_list.append(lo)
            f_list.append(f)
            plt.plot(np.arange(0,len(f)),f,label = legends[index])
            plt.xlabel("iterations")
            plt.ylabel("objective function")
            # plt.ylim(0,worst_val*1.1)
            
        plt.title(improv_names[index2])
        plt.legend()
        
    # plt.setp(ax, ylim=(min(min(f_list)),worst_val*1.1))
    # plt.savefig("../HeuOpt\\192.137-2023W\\"+".png")
    # plt.savefig("..//res/plots/"+ inst_name + ".png")
    plt.show()
    

# get best values
lo_all=[]
f_min_all = []
for f in f_list:
    lo = f.index(min(f)) 
    f_min = min(f)
    lo_all.append(lo)
    f_min_all.append(min(f))
    
stat_vertex = f_min_all[0::3]
stat_compon = f_min_all[1::3]
stat_twoexc = f_min_all[2::3]

stat_vertex2 = lo_all[0::3]
stat_compon2 = lo_all[1::3]
stat_twoexc2 = lo_all[2::3]

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









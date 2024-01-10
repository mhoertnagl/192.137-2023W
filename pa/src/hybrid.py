# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 09:55:41 2024

@author: mfischer
"""

from reader import Reader
import numpy as np
import pyomo.environ as pyo
import networkx as nx
from solution import Solution
from problem import Problem
import matplotlib.pyplot as plt
import pandas as pd
from milp_model import MILPModel
from milp_model_fast import MILPModelFast

import detcon as dc
import rancon as rc
import neighborhoods as nhs
import localsearch
import termination


reader = Reader()

# problem = reader.read("../inst/testing/test.txt")    

# problem = reader.read("../inst/testing/heur002_n_100_m_3274.txt")
problem = reader.read("../inst/tuning/heur040_n_300_m_13358.txt")

con = rc.RanCon1(problem,10)
solution = con.construct()
solution.draw()

print(solution.get_value())
print(solution.get_components())

nbh = nhs.MILPMergeComponents(nhs.Improvement.FIRST,k_max= 20,time_limit=600)
# nbh = nhs.MILPVertexMoveNeighborhoodFast(nhs.Improvement.FIRST,k_max= 50,time_limit=60)

# solution.draw()
# print(solution.get_value())
# print(solution.get_components())
# if not solution.is_feasible():
#     print('INFEASIBLE!')

ls_ter = termination.IterationTermination(1)
ls = localsearch.LocalSearch(nbh, ls_ter)
sol_values = []
sol_values.append(solution.get_value())



for i in range(100):
    # nbh.choose_first(solution)
    solution = ls.run(solution)
    solution.draw()
    sol_values.append(solution.get_value())
    if not solution.is_feasible():
        print('INFEASIBLE!')
        solution.repair()
print(solution.get_components())
plt.rcParams['figure.dpi'] = 300
plt.plot(sol_values)

# milp_sol = solution.copy()


# sol = con.construct()
# sol.draw()
# print(sol.get_value())
nbh = nhs.VertexMoveNeighborhood(nhs.Improvement.FIRST)
ls_ter = termination.IterationTermination(500)
ls = localsearch.LocalSearch(nbh, ls_ter)
solution = ls.run(solution)
solution.draw()
print(solution.get_value())
print(solution.get_components())

# reader = Reader()
# # problem = reader.read("../inst/testing/test.txt")    
# problem = reader.read("../inst/testing/heur002_n_100_m_3274.txt")
# # problem = reader.read("../inst/tuning/heur040_n_300_m_13358.txt")

# solution = Solution(problem)
# solution.draw()
# sol_values = []
# sol_values.append(solution.get_value())

# p_size = 10
# step_size = p_size # must be the same! 

# all_nodes = np.array([n for n in range(problem.n)])
# np.random.shuffle(all_nodes)
# shuffled_nodes = np.reshape(all_nodes,(10,p_size))

# for subprob in shuffled_nodes:
#     milp_model = MILPModel(solution,subprob)
#     new_solution = milp_model.solve(1200,False)
#     sol_values.append(new_solution.get_value())
#     new_solution.draw()
#     if not new_solution.is_feasible():
#         print('-'*80)
#         print('SOLUTION INFEASIBLE!!')
#         print('-'*80)    
#         new_solution.repair()
#         new_solution.draw()
#         sol_values.append(new_solution.get_value())
        
# solution.draw()

# plt.plot(sol_values)



            
    
    
    
    
    
    
    
    
    
    
    


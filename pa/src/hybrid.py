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
import os
import time


reader = Reader()

# problem = reader.read("../inst/testing/test.txt")    

# problem = reader.read("../inst/testing/heur002_n_100_m_3274.txt")

inst_names = os.listdir("../inst/tuning/")

# nbh_names = ["MILPVertexMoveNeighborhood","MILPVertexMoveNeighborhoodFast","MILPMergeComponentsFast","MILPMergeComponents"]
nbh_names = ["MILPVertexMoveNeighborhoodFast","MILPMergeComponentsFast","MILPMergeComponents"]

k_param = [5,10,15,20]
col_names = ['instance','Neighborhood','k','objective value','elapsed time']
tuning_df = pd.DataFrame(columns=col_names)   


panda_tables = []
time_limit_param= [60]
iteration_limit = 200
imp = nhs.Improvement.RANDOM
for time_limit in time_limit_param:
    for k in k_param:
        nbhs = [nhs.MILPVertexMoveNeighborhood(imp,k ,time_limit),nhs.MILPVertexMoveNeighborhoodFast(imp,k ,time_limit),nhs.MILPMergeComponentsFast(imp,k ,time_limit),nhs.MILPMergeComponents(imp,k ,time_limit)]
        for nbh in nbhs:
            for inst_name in inst_names[0:2]:
                start = time.time()
                problem = reader.read("../inst/tuning/"+inst_name)
                con = rc.RanCon1(problem,10)
                solution = con.construct()
                ls_ter = termination.IterationTermination(0)
                ls = localsearch.LocalSearch(nbh, ls_ter)
                sol_values = []
                sol_values.append(solution.get_value())
                for i in range(iteration_limit):
                    print(i)
                    # nbh.choose_first(solution)
                    solution = ls.run(solution)
                    solution.draw()
                    sol_values.append(solution.get_value())
                    if not solution.is_feasible():
                        print('INFEASIBLE!')
                        solution.repair()  
                end = time.time()
                panda_tables.append([inst_name,nbh.write(),k,solution.get_value(),end-start])                
                print([inst_name,nbh.write(),k,solution.get_value(),end-start])
                
            break
        break
    break

# write data to csv file
res_filepath = "../reshybrid/"
# tuning_df = pd.DataFrame(panda_tables, columns=col_names)      
# tuning_df.to_csv(res_filepath+"panda_res.csv")

# read from csv file
panda_res = pd.read_csv("192.137-2023W/pa/reshybrid/out.csv",sep=";")

panda_res.index = [nbh_names[i] for i in range(3) for t in range(18)]*4
panda_res.Neighborhood = [nbh_names[i] for i in range(3) for t in range(18)]*4

panda_res.boxplot(column='objective value',by='k')
panda_res.boxplot(column='objective value',by='Neighborhood')
panda_res.boxplot(column='objective value',by=['k','Neighborhood'],layout=(2, 1))



# fig, ax = plt.subplots(1,2)
plt.figure(figsize=(40, 12))
panda_res.boxplot(column='objective value',by='Neighborhood',fontsize=6)  
plt.xlabel(" ",fontsize=5)
plt.ylabel("best objective value",fontsize=8)
plt.suptitle(' ', fontsize=5)
plt.title(' ', fontsize=5)
plt.savefig(res_filepath + 'Neighborhood'+'.png', dpi=300)


plt.figure(figsize=(40, 12))
panda_res.boxplot(column='objective value',by='k',fontsize=6)  
plt.xlabel("k values",fontsize=5)
plt.ylabel("best objective value",fontsize=8)
plt.suptitle(' ', fontsize=5)
plt.title(' ', fontsize=5)
plt.savefig(res_filepath + 'k'+'.png', dpi=300)


# plt.subplot(121)
# plt.subplot(122)
# panda_res.boxplot(column='objective value',by='k')
# plt.show()
# plt.savefig("../HeuOpt\\192.137-2023W\\"+".png")


# problem = reader.read("../inst/tuning/heur040_n_300_m_13358.txt")

# con = rc.RanCon1(problem,10)
# solution = con.construct()
# solution.draw()

# print(solution.get_value())
# print(solution.get_components())




# # nbh = nhs.MILPMergeComponents(nhs.Improvement.FIRST,k_max= 5,time_limit=60)
# nbh = nhs.MILPVertexMoveNeighborhoodFast(nhs.Improvement.FIRST,k_max= 5,time_limit=60)

# solution.draw()
# print(solution.get_value())
# print(solution.get_components())
# if not solution.is_feasible():
#     print('INFEASIBLE!')

# ls_ter = termination.IterationTermination(1)
# ls = localsearch.LocalSearch(nbh, ls_ter)
# sol_values = []
# sol_values.append(solution.get_value())



# for i in range(100):
#     # nbh.choose_first(solution)
#     solution = ls.run(solution)
#     solution.draw()
#     sol_values.append(solution.get_value())
#     if not solution.is_feasible():
#         print('INFEASIBLE!')
#         solution.repair()
# print(solution.get_components())
# plt.rcParams['figure.dpi'] = 300
# plt.plot(sol_values)

# # milp_sol = solution.copy()


# # sol = con.construct()
# # sol.draw()
# # print(sol.get_value())
# nbh = nhs.VertexMoveNeighborhood(nhs.Improvement.FIRST)
# ls_ter = termination.IterationTermination(500)
# ls = localsearch.LocalSearch(nbh, ls_ter)
# solution = ls.run(solution)
# solution.draw()
# print(solution.get_value())
# print(solution.get_components())

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



            
    
    
    
    
    
    
    
    
    
    
    


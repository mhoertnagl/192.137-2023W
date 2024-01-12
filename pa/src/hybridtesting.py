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
relative_path = "../inst/testing/"
inst_names = os.listdir(relative_path)
inst_names = inst_names[:-1]
nbh_name = ["MILPMergeComponents"]

col_names = ['instance','Neighborhood','k','objective value','elapsed time']
testing_df = pd.DataFrame(columns=col_names)   


panda_tables = []
k = 15
time_limit = 20
iteration_limit = 100
imp = nhs.Improvement.RANDOM
nbh = nhs.MILPMergeComponents(imp,k,time_limit)
for inst_name in inst_names:
    start = time.time()
    problem = reader.read(relative_path+inst_name)
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
        if np.std(sol_values[-10:]) == 0:
                  if i> 40:
                      break
    end = time.time()
    panda_tables.append([inst_name,nbh.write(),k,solution.get_value(),end-start])                
    print([inst_name,nbh.write(),k,solution.get_value(),end-start])
    # plot 
    res_filepath = "../reshybrid/" 
    plt.figure(figsize=(20, 14))
    plt.title(inst_name,fontsize = 20)
    plt.xlabel("iterations",fontsize = 20)
    plt.ylabel("objective value",fontsize = 20)
    plt.plot(sol_values)
    plt.savefig(res_filepath + inst_name +'.png', dpi=300)
    plt.show()


# write data to csv file
res_filepath = "../reshybrid/"
testing_df = pd.DataFrame(panda_tables, columns=col_names,index = inst_names)      
# new_testing_df = testing_df[['Neighborhood','k','objective value','elapsed time']]
testing_df.to_latex(index = False)
testing_df.to_csv(res_filepath+"panda_res3.csv",index = False)

print(testing_df.to_latex())

# read from csv file
# panda_res = pd.read_csv(res_filepath +"out.csv",sep=";")
# panda_res.index = [nbh_names[i] for i in range(3) for t in range(18)]*4
# panda_res.Neighborhood = [nbh_names[i] for i in range(3) for t in range(18)]*4

# panda_res.boxplot(column='objective value',by='k')
# panda_res.boxplot(column='objective value',by='Neighborhood')
# panda_res.boxplot(column='objective value',by=['k','Neighborhood'],layout=(2, 1))



# # fig, ax = plt.subplots(1,2)
# plt.figure(figsize=(40, 12))
# panda_res.boxplot(column='objective value',by='Neighborhood',fontsize=6)  
# plt.xlabel(" ",fontsize=5)
# plt.ylabel("best objective value",fontsize=8)
# plt.suptitle(' ', fontsize=5)
# plt.title(' ', fontsize=5)
# plt.savefig(res_filepath + 'Neighborhood'+'.png', dpi=300)


# plt.figure(figsize=(40, 12))
# panda_res.boxplot(column='objective value',by='k',fontsize=6)  
# plt.xlabel("k values",fontsize=5)
# plt.ylabel("best objective value",fontsize=8)
# plt.suptitle(' ', fontsize=5)
# plt.title(' ', fontsize=5)
# plt.savefig(res_filepath + 'k'+'.png', dpi=300)


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



            
    
    
    
    
    
    
    
    
    
    
    


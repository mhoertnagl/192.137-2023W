# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 19:35:17 2023

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


class MILPModelFast:
    def __init__(self, solution: Solution, subprob: list):
        self.solution = solution
        self.problem = solution.prob
        
        # parameter definition
        N = np.array([n for n in subprob]) # array of vertices from subproblem
        V = len(subprob) # number of vertices of subproblem 
        self.V = V
        s = self.problem.s #splex
        self.N = N
        # read weights and give the original edges negative values
        W = pd.DataFrame(np.copy(self.problem.get_weights()),index=range(1,self.problem.n+1),columns=range(1,self.problem.n+1)) 
        for i,j in self.problem.edges:
            W[i][j] = - W[i][j]
            W[j][i] =  -W[j][i]
        
        self.m = self.create_model(N, V, s, W)
    
    def create_model(self, N, V, s, W):                    
        # model definition 
        m = pyo.ConcreteModel()
        m.N = pyo.Set(initialize=N)
        m.A = pyo.Var(m.N,m.N,domain=pyo.Binary)
        
        # define constraints
        m.cons = pyo.ConstraintList()
        
        for n in N:
            m.cons.add(expr= sum(m.A[n,:])>= V-s)  # |S| - s constraint
            m.cons.add(expr = m.A[n,n] == 0)            # diag(A) = 0!
             
            for j in N:
                m.cons.add(expr = m.A[n,j] == m.A[j,n])  # A matrix must be diagonal                         
       
                    
        # objective
        m.obj = pyo.Objective(expr = sum(m.A[n,j]*W[n][j] for n in N for j in N), sense=pyo.minimize)
        return m
        
    def solve(self, time_limit: int = 1000,tee_value: bool= False):
        # solve
        solver = pyo.SolverFactory('gurobi')
        solver.options['timelimit'] = time_limit
        # results = solver.solve(self.m, timelimit = time_limit)
        results = solver.solve(self.m, tee=tee_value,options = {'threads':8, 'timelimit':time_limit}) 
        print('solved in {:4.3} seconds'.format(results.Solver.Time))   
        A_solved = pd.DataFrame(np.reshape(self.m.A[:,:](),(self.V,self.V)),index=self.N,columns=self.N)    

        for i in self.N:
            for j in self.N:
                if(A_solved[i][j]==1):
                    self.solution.add_edge(i,j)
                if(A_solved[i][j]==0):
                    self.solution.remove_edge(i,j)
        return self.solution, A_solved
              
       
# reader = Reader()
# # problem = reader.read("../inst/testing/test.txt")    
# problem = reader.read("../inst/testing/heur002_n_100_m_3274.txt")
# # problem = reader.read("../inst/tuning/heur040_n_300_m_13358.txt")

# solution = Solution(problem)
# sol_values = []
# sol_values.append(solution.get_value())

# p_size = 10
# step_size = p_size # must be the same! 

# all_nodes = np.array([n for n in range(problem.n)])
# np.random.shuffle(all_nodes)
# shuffled_nodes = np.reshape(all_nodes,(10,p_size))

# for subprob in shuffled_nodes:
#     milp_model = MILPModel(solution,subprob)
#     solution, A_solved = milp_model.solve(60,False)
#     sol_values.append(solution.get_value())
#     solution.draw()
#     if not solution.is_feasible():
#         print('-'*80)
#         print('SOLUTION INFEASIBLE!!')
#         print('-'*80)
#         break


# plt.plot(sol_values)



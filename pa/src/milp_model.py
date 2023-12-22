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

class MILPModel:
    def __init__(self, problem: Problem):
        self.problem = problem
    # parameter definition
        V = self.problem.n #number of vertices
        self.V = V
        N = np.array([t for t in range(0,V)]) # nodes
        s = self.problem.s #splex
        W = self.problem.weights
        M = V
        self.N = N

        for i,j in self.problem.edges:
            W[i-1,j-1] = - W[i-1,j-1]
            W[j-1,i-1] =  -W[j-1,i-1]
        
        self.m = self.create_model(N, V, s, M, W)
    
    def create_model(self, N, V, s, M, W):                    
        # model definition 
        m = pyo.ConcreteModel()
        m.N = pyo.Set(initialize=N) 
        m.A = pyo.Var(m.N,m.N,domain=pyo.Binary)
        m.B = pyo.Var(m.N,m.N,domain=pyo.Binary)
        m.Bt= pyo.Var(m.N,m.N,domain=pyo.Binary)
        m.Bm= pyo.Var(m.N,m.N,domain=pyo.Binary)
        m.k = pyo.Var(m.N,domain=pyo.Integers)
        m.p = pyo.Var(m.N,domain = pyo.Reals)
        m.u = pyo.Var(m.N,domain=pyo.Binary)
        
        # define constraints
        m.cons = pyo.ConstraintList()
        m.cons.add(expr = sum(m.B[n,j] for n in N for j in N) == V) # every node can only be assigned once
        
        
        for n in N:
            m.cons.add(expr= sum(m.A[n,:])>= m.p[n]-s)
            m.cons.add(expr = m.A[n,n] == 0)            # diag(A) = 0!
            m.cons.add(expr = sum(m.B[n,j] for j in N) == 1) # only one node per line
            m.cons.add(expr = m.k[n] == sum(m.B[:,n]))
            m.cons.add(expr = m.u[n] <= m.k[n])
            m.cons.add(expr = m.u[n] >= (m.k[n]-1)/M)
            m.cons.add(expr = m.p[n] == sum(m.Bm[n,l] for l in N))    
            for j in N:
                m.cons.add(expr = m.A[n,j] == m.A[j,n])  # A matrix must be diagonal
                m.cons.add(expr = m.Bt[n,j] == m.B[j,n]) # transpose B matrix            
        for b in N:
            for i in N[:-1]:
                for j in range(min(i+1,V),V):
                    m.cons.add(expr = m.A[i,j] <= 1 - (m.B[i,b]-m.B[j,b]))
                    m.cons.add(expr = m.A[i,j] <= 1 - (m.B[j,b]-m.B[i,b]))  
        for j in N:    
            for i in N:   
                m.cons.add(expr = m.Bm[i,j] == sum(m.B[i,l]*m.Bt[l,j] for l in N))
        for n in N[:-1]:
            m.cons.add(expr = m.k[n] >= m.k[n+1])
            
            
        # objective
        m.obj = pyo.Objective(expr = sum(m.A[n,j]*W[n,j] for n in N for j in N), sense=pyo.minimize)
        return m
        
    def solve(self, time_limit: int = 1000,tee_value: bool= False):
        # solve
        solver = pyo.SolverFactory('gurobi')
        solver.options['timelimit'] = time_limit
        results = solver.solve(self.m, timelimit = time_limit)
        results = solver.solve(self.m, tee=tee_value,options = {'timelimit':time_limit})
        print('solved in {:4.3} seconds'.format(results.Solver.Time))      
        A_solved = np.reshape(self.m.A[:,:](),(self.V,self.V))       
        solution = Solution(self.problem)
        for i in self.N:
            for j in self.N:
                if(A_solved[i,j]==1):
                    solution.add_edge(i+1,j+1)
        return solution
            
       
reader = Reader()
problem = reader.read("../inst/testing/test.txt")
milp_model = MILPModel(problem)
solution = milp_model.solve(100,False)
solution.draw()
    
    

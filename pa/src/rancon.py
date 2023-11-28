# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 15:45:42 2023

@author: Martin
"""

from abc import ABC, abstractmethod
from problem import Problem
from solution import Solution
import random


class RanCon(ABC):

    @abstractmethod
    def construct(self) -> Solution:
        pass


class RanCon1(RanCon, ABC):

    def __init__(self, prob: Problem, k: int):
        self.prob = prob
        self.k = k
        self.sol = Solution(prob)
        # For the initial empty solution, every vertex
        # is a singular component.
        n = self.prob.n + 1
        self.components = [{i} for i in range(1, n)]

    def construct(self) -> Solution:
        # edges = self.prob.initial_edges_weighted(reverse=True)
        edges = self.prob.all_edges_weighted(reverse=True)
        ran_edges = self.random_shuffle(edges)
                
        for (_, u, v) in ran_edges:
            # Find the components that contain u and v
            # respectively. Maybe the same component.
            cu = self.component(u)
            cv = self.component(v)
            # The union would be the new component if we add
            # edge (u,v).
            # Add the smaller set to the larger one.
            cn = cu.union(cv) if len(cu) > len(cv) else cv.union(cu)
            # Find the minimum degree of all vertices in the
            # unified component. For vertices u and v the degree
            # is incremented by because of the new edge added.
            min_component_degree = self.min_degree(cn, u, v)
            # Subtracting s yields the minimum required degree
            # for the unified component.
            min_required_degree = len(cn) - self.prob.s
            # s-plex property is met if the minimum degree of
            # unified component is greater or equal to the
            # required degree.
            if min_component_degree > min_required_degree:
                self.sol.add_edge(u, v)
                # Update the connected components.
                self.components = self.sol.get_components()
        return self.sol

    def random_shuffle(self, edges: list):
        # Partition list of edges in k long sub-lists.
        p_edges = [edges[i:i + self.k] for i in range(0, len(edges), self.k)]
        # Shuffle each sublist.
        for i in range(len(p_edges)):
            random.shuffle(p_edges[i]) 
        # Merge partitioned list.
        shuffled_edges = [j for i in p_edges for j in i]
        return shuffled_edges
    
    # Get the minimum degree node for a connected component.
    def min_degree(self, c: set, x: int, y: int) -> int:
        return min(map(lambda v: self.degree(v, x, y), c))

    # Get the degree for vertex v and the degree
    # plus one if v is x or y.
    def degree(self, v: int, x: int, y: int):
        d = self.sol.degree(v)
        return d+1 if v == x or v == y else d

    # Get the component that contains vertex v.
    def component(self, v: int) -> set:
        for c in self.components:
            if v in c:
                return c
        return set()


# class RanCon2(RanCon, ABC):
#
#     def __init__(self, prob: Problem):
#         self.prob = prob
#         self.sol = Solution(prob)
#         # For the initial empty solution, every vertex
#         # is a singular component.
#         n = self.prob.n + 1
#         self.components = [{i} for i in range(1, n)]
#
#     def construct(self) -> Solution:
#         edges = self.prob.initial_edges_weighted(reverse=True)
#
#         for (_, u, v) in edges:

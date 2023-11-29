import random
from typing import Iterable

import networkx as nx

from abc import ABC, abstractmethod
from problem import Problem
from solution import Solution


class DetCon(ABC):

    @abstractmethod
    def construct(self) -> Solution:
        pass


class DetCon1(DetCon, ABC):

    def __init__(self, prob: Problem):
        self.prob = prob
        self.sol = Solution(prob)
        # For the initial empty solution, every vertex
        # is a singular component.
        n = self.prob.n + 1
        self.components = [{i} for i in range(1, n)]

    def construct(self) -> Solution:
        edges = self.prob.initial_edges_weighted(reverse=True)
        for (_, u, v) in edges:
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
            # unified component is greater than the required
            # degree.
            if min_component_degree > min_required_degree:
                self.sol.add_edge(u, v)
                # Update the connected components.
                self.components = self.sol.get_components()
        return self.sol

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


class DetCon2(DetCon, ABC):

    def __init__(self, prob: Problem):
        self.prob = prob
        self.sol = Solution(prob)

    def construct(self) -> Solution:
        for (_, i, j) in self.prob.all_edges_weighted():
            self.sol.add_edge(i, j)
            if not self.sol.is_feasible():
                self.sol.remove_edge(i, j)
        return self.sol


# class DetCon3(DetCon, ABC):
#
#     def __init__(self, prob: Problem):
#         self.prob = prob
#         self.sol = Solution(prob, empty=False)
#
#     # TODO: Could be used as a neighborhood structure.
#     def construct(self):
#         # x = dict(nx.all_pairs_shortest_path(self.sol.graph))
#         x = nx.triangles(self.sol.graph)
#         cs = self.sol.get_components()
#         # print(self.sol.is_feasible())
#         for c in cs:
#             b = len(c) - self.prob.s
#             # Nodes with too low degree.
#             vs = {v for v in c if self.sol.degree(v) < b}
#             ds = {v: self.sol.degree(v) - b for v in vs}
#             # All edges in this component.
#             ces = set(self.sol.get_edges(c))
#             # Existing edges among these nodes.
#             xes = set(self.sol.get_edges(vs))
#             # Sort by weight.
#             res = self.prob.edges_weighted(ces.difference(xes))
#             # If both vertices are below s-plex, add
#             # an edge between them.
#             for (_, u, v) in res:
#                 if ds[u] < 0 and ds[v] < 0:
#                     self.sol.graph.add_edge(u, v)
#                     ds[u] += 1
#                     ds[v] += 1
#             # If either vertex but not the other are
#             # below s-plex, add an edge to this vertex.
#             for (_, u, v) in res:
#                 if ds[u] < 0:
#                     self.sol.graph.add_edge(u, v)
#                     ds[u] += 1
#                 if ds[v] < 0:
#                     self.sol.graph.add_edge(u, v)
#                     ds[v] += 1
#         return self.sol

import numpy as np
import networkx as nx


# class DeterministicConstructor:
#     """
#
#     """
#
#     def __init__(self, G, s):
#         self.G = G
#         self.s = s
#         # Fully connect graph
#         self.f = self.evaluate()
#         # Sort edges descending to weight
#         self.edges = self.G.edges()
#         [(1, 2, ), (2, 3)]
#
#     def construct(self):
#         deleted = True
#         while deleted:
#             deleted = False
#             for (i, j) in self.edges:
#                 f2 = 0 # Compute new f
#                 if self.is_feasible(i) and self.is_feasible(j) and f2 < self.f:
#                     deleted = True
#                     self.G.remove_edge((i, j))
#                     self.edges.remove((i, j))
#                     self.f = f2
#
#     def is_feasible(self, v: int):
#         for component in nx.connected_components(self.G):
#             if v in component:
#                 # Subtract one because we are interested if
#                 # the degree without the removed edge is
#                 # still at least b.
#                 return self.G.degree(v)-1 >= len(component) - self.s
#         return False
#
#     def evaluate(self):
#         return 0

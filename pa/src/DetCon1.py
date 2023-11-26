import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from Problem import Problem
from Solution import Solution


class DetCon1:

    def __init__(self, problem: Problem):
        self.__problem = problem
        self.__solution = Solution(problem)
        # TODO: Replace with custom data structure.
        self.__components: list[set] = self.__solution.components()

    def construct(self):
        edges = self.__problem.initial_edges_weighted(reverse=True)
        for (_, u, v) in edges:
            # Find the components that contain u and v
            # respectively. Maybe the same component.
            cu = self.component(u)
            cv = self.component(v)
            # The union would be the new component if we add
            # edge (u,v).
            # TODO: Take set sizes into account.
            cn = cu.union(cv)
            # Find the minimum degree of all vertices in the
            # unified component. For vertices u and v the degree
            # is incremented by because of the new edge added.
            min_component_degree = self.min_degree(cn, u, v)
            # Subtracting s yields the minimum required degree
            # for the unified component.
            min_required_degree = len(cn) - self.__problem.s
            # s-plex property is met if the minimum degree of
            # unified component is greater or equal to the
            # required degree.
            if min_component_degree >= min_required_degree:
                self.__solution.add_edge(u, v)
                # Update the connected components.
                # TODO: Use custom data structure for increased speed.
                self.__components = self.__solution.components()
        return self.__solution

    # Get the minimum degree node for a connected component.
    def min_degree(self, c: set, x: int, y: int) -> int:
        return min(map(lambda v: self.degree(v, x, y), c))

    # Get the degree for vertex v and the degree
    # plus one if v is x or y.
    def degree(self, v: int, x: int, y: int):
        d = self.__solution.degree(v)
        return d+1 if v == x or v == y else d

    # Get the component that contains vertex v.
    def component(self, v: int) -> set:
        for c in self.__components:
            if v in c:
                return c
        return set()

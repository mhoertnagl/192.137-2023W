import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from Problem import Problem


class Solution:

    def __init__(self, problem: Problem):
        self.__problem = problem
        self.__graph = nx.Graph()
        self.__graph.add_nodes_from(range(1, problem.n))

    def add_edge(self, u: int, v: int):
        return self.__graph.add_edge(u, v)

    def remove_edge(self, u: int, v: int):
        return self.__graph.remove_edge(u, v)

    def has_edge(self, u: int, v: int):
        # m0, m1 = min(u, v), max(u, v)
        # return self.__graph.has_edge(m0, m1)
        return self.__graph.has_edge(u, v)

    def edge_edited(self, u: int, v: int):
        return self.has_edge(u, v) != self.__problem.has_edge(u, v)

    def components(self) -> list[set]:
        return list(nx.connected_components(self.__graph))

    def degree(self, v: int):
        return self.__graph.degree(v)

    def is_feasible(self):
        s = self.__problem.s
        for component in self.components():
            size = len(component)
            for v in component:
                if self.degree(v) < size - s:
                    return False
        return True

    def is_vertex_feasible(self, v: int):
        s = self.__problem.s
        for component in self.components():
            if v in component:
                size = len(component)
                return self.degree(v) >= size - s
        return False

    def evaluate(self):
        f = 0
        n = self.__problem.n+1
        for i in range(1, n):
            for j in range(i+1, n):
                if self.edge_edited(i, j):
                    f += self.__problem.weight(i, j)
        return f

    def draw(self):
        nx.draw(self.__graph, with_labels=True, font_weight='bold')
        plt.show()

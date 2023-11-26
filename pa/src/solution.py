import pandas as pd
import numpy as np
import pymhlib as mh
import networkx as nx
import matplotlib.pyplot as plt

from problem import Problem


class Solution:

    def __init__(self, problem: Problem):
        self.__problem = problem
        self.__graph = nx.Graph()
        self.__graph.add_nodes_from(range(1, problem.n))
        self.__value = self.evaluate()
        self.__components = self.components()
        self.__value_valid = True
        self.__components_valid = True

    def copy(self):
        new_solution = Solution(self.__problem)
        new_solution.__graph = self.__graph.copy()
        return new_solution

    def num_of_vertices(self):
        return self.__problem.n

    def add_edge(self, u: int, v: int):
        self.__value_valid = False
        self.__components_valid = False
        return self.__graph.add_edge(u, v)

    def remove_edge(self, u: int, v: int):
        self.__value_valid = False
        self.__components_valid = False
        return self.__graph.remove_edge(u, v)

    def random_edge_from_all(self) -> (int, int):
        i = np.random.random_integers(1, self.num_of_vertices())
        return self.__problem.all_edges[i]

    def has_edge(self, u: int, v: int):
        return self.__graph.has_edge(u, v)

    def edge_edited(self, u: int, v: int):
        return self.has_edge(u, v) != self.__problem.has_edge(u, v)

    def components(self) -> list[set[int]]:
        # if not self.__components_valid:
        self.__components = list(nx.connected_components(self.__graph))
        #    self.__components_valid = True
        return self.__components

    def degree(self, v: int) -> int:
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

    def delta_evaluate(self, edges: list[(int, int)]):
        pass

    def draw(self):
        nx.draw(self.__graph, with_labels=True, font_weight='bold')
        plt.show()

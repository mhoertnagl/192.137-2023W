import pandas as pd
import numpy as np
import pymhlib as mh
import networkx as nx
import matplotlib.pyplot as plt

from problem import Problem


class Solution:
    def __init__(self, prob: Problem):
        self.prob = prob
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(1, prob.n))
        # An empty solution has all initial edges deleted.
        # self.changeset = set(prob.edges)
        # print(self.changeset)
        # print(prob.all_edges)
        self.value_valid = False
        # self.value = self.evaluate()
        self.__value = self.get_value()
        self.components_valid = False
        self.__components = self.get_components()

    def copy(self):
        sol = Solution(self.prob)
        sol.graph = self.graph.copy()
        return sol

    def num_of_vertices(self):
        return self.prob.n

    def add_edge(self, u: int, v: int):
        self.value_valid = False
        self.components_valid = False
        # Add edge.
        self.graph.add_edge(u, v)
        # if not self.graph.has_edge(u, v):
        #     # Update changeset.
        #     if self.prob.has_edge(u, v):
        #         # Add an initial vertex.
        #         if (u, v) in self.changeset:
        #             self.changeset.remove((u, v))
        #             self.value -= self.prob.weight(u, v)
        #     else:
        #         # Add an additional vertex.
        #         if not (u, v) in self.changeset:
        #             self.changeset.add((u, v))
        #             self.value += self.prob.weight(u, v)
        #     # Invalidate computed values.
        #     # self.value_valid = False
        #     self.components_valid = False
        #     # Add edge.
        #     self.graph.add_edge(u, v)

    def remove_edge(self, u: int, v: int):
        self.value_valid = False
        self.components_valid = False
        # Remove edge.
        self.graph.remove_edge(u, v)
        # if self.graph.has_edge(u, v):
        #     # Update changeset.
        #     if self.prob.has_edge(u, v):
        #         # Remove an initial edge.
        #         if not (u, v) in self.changeset:
        #             self.changeset.add((u, v))
        #             self.value += self.prob.weight(u, v)
        #     else:
        #         # Remove an additional edge.
        #         if (u, v) in self.changeset:
        #             self.changeset.remove((u, v))
        #             self.value -= self.prob.weight(u, v)
        #     # Invalidate computed values.
        #     # self.value_valid = False
        #     self.components_valid = False
        #     # Remove edge.
        #     self.graph.remove_edge(u, v)

    def toggle_edge(self, u: int, v: int):
        if self.has_edge(u, v):
            return self.remove_edge(u, v)
        else:
            return self.add_edge(u, v)

    def random_edge_from_all(self) -> (int, int):
        i = np.random.randint(0, len(self.prob.all_edges))
        return self.prob.all_edges[i]

    def has_edge(self, u: int, v: int):
        return self.graph.has_edge(u, v)

    def edge_edited(self, u: int, v: int):
        return self.has_edge(u, v) != self.prob.has_edge(u, v)

    def get_neighbors(self, v: int):
        return self.graph.neighbors(v)

    # def get_edges(self, nbunch: any):
    #     return self.

    def get_components(self) -> list[set[int]]:
        if not self.components_valid:
            self.__components = self.__get_components()
            self.components_valid = True
        return self.__components

    def __get_components(self) -> list[set[int]]:
        return list(nx.connected_components(self.graph))

    def get_random_component(self) -> set[int]:
        components = self.get_components()
        i = np.random.randint(0, len(components))
        return components[i]

    def degree(self, v: int) -> int:
        return self.graph.degree(v)

    def is_feasible(self):
        for c in self.get_components():
            sz = len(c)
            for v in c:
                if self.degree(v) < sz - self.prob.s:
                    return False
        return True

    def is_vertex_feasible(self, v: int):
        for c in self.get_components():
            if v in c:
                return self.degree(v) >= len(c) - self.prob.s
        return False

    def get_value(self):
        if not self.value_valid:
            self.__value = self.__get_value()
            self.value_valid = True
        return self.__value

    def __get_value(self):
        # return sum([self.prob.weight(i, j) for (i, j) in self.changeset])
        # f = 0
        # for (i, j) in self.changeset:
        #     f += self.prob.weight(i, j)
        # return f
        f, n = 0, self.prob.n + 1
        for i in range(1, n):
            for j in range(i+1, n):
                if self.edge_edited(i, j):
                    f += self.prob.weight(i, j)
        return f

    def delta_evaluate(self, edges: list[(int, int)]):
        pass

    def weight(self, u: int, v: int):
        return self.prob.weight(u, v)

    def worst_value(self):
        return self.prob.worst_value()

    def draw(self):
        nx.draw(self.graph, with_labels=True, font_weight='bold')
        plt.show()

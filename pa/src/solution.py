import os
from io import StringIO

import pandas as pd
import numpy as np
import pymhlib as mh
import networkx as nx
import matplotlib.pyplot as plt

from problem import Problem


class Solution:

    def __init__(self, prob: Problem, empty=True):
        self.prob = prob
        if empty:
            self.graph = nx.Graph()
            self.graph.add_nodes_from(range(1, prob.n+1))
        else:
            self.graph = prob.graph.copy()
        self.__value = self.__get_value()
        self.components_valid = False
        self.__components = self.__get_components()

    def copy(self):
        sol = Solution(self.prob)
        sol.graph = self.graph.copy()
        sol.__value = self.__get_value()
        return sol

    def num_of_vertices(self):
        return self.prob.n

    def add_edge(self, u: int, v: int):
        if not self.graph.has_edge(u, v):
            if self.prob.has_edge(u, v):
                self.__value -= self.prob.weight(u, v)
            else:
                self.__value += self.prob.weight(u, v)
            self.components_valid = False
            self.graph.add_edge(u, v)

    def add_edges(self, es: list[(int, int)]):
        for (u, v) in es:
            self.add_edge(u, v)

    def remove_edge(self, u: int, v: int):
        if self.graph.has_edge(u, v):
            if self.prob.has_edge(u, v):
                self.__value += self.prob.weight(u, v)
            else:
                self.__value -= self.prob.weight(u, v)
            self.components_valid = False
            self.graph.remove_edge(u, v)

    def remove_edges(self, es: list[(int, int)]):
        for (u, v) in es:
            self.remove_edge(u, v)

    def toggle_edge(self, u: int, v: int):
        if self.has_edge(u, v):
            self.remove_edge(u, v)
        else:
            self.add_edge(u, v)

    def random_edge_from_all(self) -> (int, int):
        i = np.random.randint(0, len(self.prob.all_edges))
        return self.prob.all_edges[i]

    def has_edge(self, u: int, v: int):
        return self.graph.has_edge(u, v)

    def edge_edited(self, u: int, v: int):
        return self.has_edge(u, v) != self.prob.has_edge(u, v)

    def edge_added(self, u: int, v: int):
        return self.has_edge(u, v) and not self.prob.has_edge(u, v)

    def edge_deleted(self, u: int, v: int):
        return not self.has_edge(u, v) and self.prob.has_edge(u, v)

    def get_neighbors(self, v: int):
        return self.graph.neighbors(v)

    def get_neighbors_weighted(self, v: int):
        nv = self.graph.neighbors(v)
        w = [self.weight(n, v) for n in nv]
        wn = [x for _,x in sorted(zip(w,nv))]
        return wn

    def get_edges_weighted(self, v: int, u: list):
        w = [self.weight(v, n) for n in u]
        wn = [x for _,x in sorted(zip(w,u))]
        return wn
    
    def get_solution_edges(self):
        return self.graph.edges

    def get_edges(self, vs: set[int]):
        return [(u, v) for (u, v) in self.graph.edges
                       if u in vs and v in vs]

    def get_edges_between(self, us: set[int], vs: set[int]):
        return [(u, v) for (u, v) in self.graph.edges
                       if u in us and v in vs]

    def get_edges_between_ordered_by_weight(self,
                                            us: set[int],
                                            vs: set[int],
                                            reverse=False):
        ws = [(self.weight(u, v), u, v) for (u, v) in self.graph.edges
                                        if u in us and v in vs]
        ws.sort(reverse=reverse)
        return ws

    def get_components(self) -> list[set[int]]:
        # if not self.components_valid:
        #     self.__components = self.__get_components()
        #     self.components_valid = True
        # return self.__components
        return self.__get_components()

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
        return self.__value

    def __get_value(self):
        f, n = 0, self.prob.n + 1
        for i in range(1, n):
            for j in range(i + 1, n):
                if self.edge_edited(i, j):
                    f += self.prob.weight(i, j)
        return f

    def delta(self, add: list[(int, int)], rem: list[(int, int)]) -> int:
        df = 0
        for (u, v) in add:
            if self.prob.has_edge(u, v):
                df -= self.prob.weight(u, v)
            else:
                df += self.prob.weight(u, v)
        for (u, v) in rem:
            if self.prob.has_edge(u, v):
                df += self.prob.weight(u, v)
            else:
                df -= self.prob.weight(u, v)
        return df

    def weight(self, u: int, v: int):
        return self.prob.weight(u, v)

    def worst_value(self):
        return self.prob.worst_value()

    def draw(self):
        nx.draw(self.graph, with_labels=True, font_weight='bold')
        plt.show()

    def __str__(self):
        s = StringIO()
        s.write(f"{self.prob.name}\n")
        for (u, v) in self.get_solution_edges():
            if self.edge_edited(u, v):
                s.write(f"{u} {v}\n")
        return s.getvalue()

    def write(self, out_dir: str):
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"{self.prob.name}.txt")
        with open(filename, "w") as file:
            file.write(self.__str__())

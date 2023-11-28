from io import StringIO
from typing import Iterable

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Problem:

    def __init__(self, name: str, s: int, n: int, edges: list):
        self.name = name     # Problem instance name.
        self.s = s           # s-plex number.
        self.n = n           # Number of vertices.
        self.graph = nx.Graph()  # Input graph.
        self.weights = np.zeros((n, n), dtype=int)
        self.edges = set()
        self.all_edges = []
        self.__inti_edges(edges)
        self.__init_all_edges()
        self.__init_edges()

    def __inti_edges(self, edges: list):
        for (u, v, p, w) in edges:
            if p == 1:
                self.graph.add_edge(u, v)
                # self.graph.add_weighted_edges_from([(u, v, w)])
            self.weights[u - 1, v - 1] = w

    def __init_all_edges(self):
        for i in range(1, self.n+1):
            for j in range(i+1, self.n+1):
                self.all_edges.append((i, j))

    def __init_edges(self):
        self.edges = {tuple(sorted(t)) for t in self.graph.edges()}

    def has_edge(self, u: int, v: int):
        return self.graph.has_edge(u, v)

    def weight(self, u: int, v: int):
        m0, m1 = min(u, v), max(u, v)
        return self.weights[m0 - 1, m1 - 1]

    def initial_edges_weighted(self, reverse=False):
        return self.edges_weighted(self.edges, reverse)

    def non_edges_weighted(self, reverse=False):
        others = set(self.all_edges).difference(self.edges)
        return self.edges_weighted(others, reverse)

    def all_edges_weighted(self, reverse=False):
        return self.edges_weighted(self.all_edges, reverse)
        # edges = []
        # for (i, j) in self.all_edges:
        #     w = self.weight(i, j)
        #     # If it is an initial edge take the negated weight.
        #     w = -w if self.has_edge(i, j) else w
        #     edges.append((w, i, j))
        # return sorted(edges, reverse=reverse)

    def edges_weighted(self, es: Iterable, reverse=False):
        edges = []
        for (i, j) in es:
            w = self.weight(i, j)
            # If it is an initial edge take the negated weight.
            w = -w if self.has_edge(i, j) else w
            edges.append((w, i, j))
        return sorted(edges, reverse=reverse)

    def non_edges(self):
        return nx.non_edges(self.graph)

    def worst_value(self):
        f = 0
        for (i, j) in self.all_edges:
            f += self.weight(i, j)
        return f

    def __str__(self):
        s = StringIO()
        s.write(f"Name: {self.name}\n")
        s.write(f"s-plex number: {self.s}\n")
        s.write(f"Number of nodes: {self.n}\n")
        s.write(f"Worst value: {self.worst_value()}\n")
        # s.write("Adjacency matrix A:\n")
        # s.write(self.__initial_adjacency_matrix.__str__())
        # s.write("\n")
        # s.write("Weights matrix W:\n")
        # s.write(self.weights.__str__())
        # s.write("\n")
        return s.getvalue()

    def draw(self):
        nx.draw(self.graph, with_labels=True, font_weight='bold')
        plt.show()
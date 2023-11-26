import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Problem:

    def __init__(self, name: str, s: int, n: int, edges: list):
        self.name = name     # Problem instance name.
        self.s = s           # s-plex number.
        self.n = n           # Number of vertices.
        self.__graph = nx.Graph()  # Input graph.
        # self.H = nx.Graph()  # Fully connected graph.
        # self.__neighbors = np.zeros((n, n), dtype=bool)  # Initial adjacency matrix.
        self.__weights = np.zeros((n, n), dtype=int)
        self.__inti_edges(edges)

    def __inti_edges(self, edges: list):
        for (u, v, p, w) in edges:
            if p == 1:
                self.__graph.add_edge(u, v)
            # self.H.add_edge(u, v)
            # self.__neighbors[u-1, v-1], = p == 1
            self.__weights[u-1, v-1] = w

    def has_edge(self, u: int, v: int):
        # m0, m1 = min(u, v), max(u, v)
        # return self.__graph.has_edge(m0, m1)
        return self.__graph.has_edge(u, v)

    def weight(self, u: int, v: int):
        m0, m1 = min(u, v), max(u, v)
        return self.__weights[m0-1, m1-1]

    def edges(self):
        return self.__graph.edges()

    def initial_edges_weighted(self, reverse=False):
        edges = [(self.weight(u, v), u, v) for (u, v) in self.edges()]
        return sorted(edges, reverse=reverse)

    def all_edges_weighted(self, reverse=False):
        edges = []
        for i in range(1, self.n+1):
            for j in range(i+1, self.n+1):
                w = self.weight(i, j)
                # If it is an initial edge take the negated weight.
                w = -w if self.has_edge(i, j) else w
                edges.append((-w, i, j))
        return sorted(edges, reverse=reverse)

    def draw(self):
        nx.draw(self.__graph, with_labels=True, font_weight='bold')
        plt.show()
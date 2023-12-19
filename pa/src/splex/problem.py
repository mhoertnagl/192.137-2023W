from abc import ABC

import numpy as np

from benchy import IProblem


class Problem(IProblem, ABC):

    def __init__(self,
                 name: str,
                 s: int,
                 n: int,
                 edges: list[(int, int, int, int)]):
        self._name = name
        self.s = s  # s-plex number.
        self.n = n  # Number of vertices.
        self._initial_edges: list[(int, int, int)] = []
        self._non_edges: list[(int, int, int)] = []
        self._all_edges: list[(int, int, int)] = []
        self._weights = np.zeros((n, n), dtype=int)
        self._adjacent = np.zeros((n, n), dtype=int)
        self._init(edges)

    def _init(self, edges: list[(int, int, int, int)]):
        for (u, v, p, w) in edges:
            if p == 1:
                self._adjacent[u-1, v-1] = 1
                self._adjacent[v-1, u-1] = 1
                self._weights[u-1, v-1] = -w
                self._weights[v-1, u-1] = -w
                self._initial_edges.append((-w, u, v))
                self._all_edges.append((-w, u, v))
            else:
                self._weights[u-1, v-1] = w
                self._weights[v-1, u-1] = w
                self._non_edges.append((w, u, v))
                self._all_edges.append((w, u, v))
        self._initial_edges.sort()
        self._non_edges.sort()
        self._all_edges.sort()

    def name(self):
        return self._name

    def has_edge(self, u: int, v: int) -> bool:
        return self._adjacent[u-1, v-1] == 1

    def weight(self, u: int, v: int) -> int:
        return self._weights[u-1, v-1]

    def initial_edges(self):
        return self._initial_edges

    def all_edges(self):
        return self._all_edges

    def non_edges(self):
        return self._non_edges
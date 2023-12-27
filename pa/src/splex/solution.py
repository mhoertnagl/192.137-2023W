from abc import ABC

import numpy as np

from benchy import ISolution
from splex import Problem
from splex.graph import Graph


class Solution(ISolution, ABC):

    def __init__(self, problem: Problem):
        self._problem = problem
        self._graph = Graph(problem.n)
        self._feasible = np.zeros(problem.n, dtype=bool)
        self._value = 0  # self._value

    def value(self) -> int | float:
        return self._value

    def delta(self, add: list[(int, int)], rem: list[(int, int)]) -> int:
        df = 0
        for (u, v) in add:
            if not self._graph.connected(u, v):
                if self._problem.connected(u, v):
                    df -= self._problem.weight(u, v)
                else:
                    df += self._problem.weight(u, v)
        for (u, v) in rem:
            if self._graph.connected(u, v):
                if self._problem.connected(u, v):
                    df += self._problem.weight(u, v)
                else:
                    df -= self._problem.weight(u, v)
        return df

    def connected(self, u: int, v: int):
        return self._graph.connected(u, v)

    def add_edges(self, es: list[(int, int)]):
        self._value += self.delta(es, [])
        self._graph.add_edges(es)

    def add_edge(self, u: int, v: int):
        self._value += self.delta([(u, v)], [])
        self._graph.add_edge(u, v)

    def remove_edges(self, es: list[(int, int)]):
        self._value += self.delta([], es)
        self._graph.remove_edges(es)

    def remove_edge(self, u: int, v: int):
        self._value += self.delta([], [(u, v)])
        self._graph.remove_edge(u, v)

    def degree(self, v: int):
        return self._graph.degree(v)

    def neighbors(self, v: int):
        return self._graph.neighbors(v)

    def components(self):
        return self._graph.components()

    def component(self, v: int):
        return self._graph.component(v)

    def is_feasible(self):
        for v in range(1, self._problem.n+1):
            if not self.is_vertex_feasible(v):
                return False
        return True

    def is_vertex_feasible(self, v: int):
        c = self._graph.component(v)
        deg = self._graph.degree(v)
        return deg >= len(c) - self._problem.s

    # def _value(self) -> int:
    #     P = self._problem._adjacent
    #     S = self._graph._adjacent
    #     W = self._problem._weights
    #     D = np.multiply(np.absolute(P - S), W)
    #     return np.sum(D)

        # f, n = 0, self._problem.n + 1
        # for i in range(1, n):
        #     for j in range(i + 1, n):
        #         if self.edge_edited(i, j):
        #             f += self._problem.weight(i, j)
        # return f


from abc import ABC
from io import StringIO

import numpy as np

from benchy import ISolution
from splex import Problem
from splex.graph import Graph


class Solution(ISolution, ABC):

    def __init__(self, problem: Problem):
        self._problem = problem
        self._graph = Graph(problem.n)
        # self._feasible = np.zeros(problem.n, dtype=bool)
        self._value = self._compute_value()

    def value(self) -> int | float:
        return self._value

    def _compute_value(self) -> int | float:
        value = 0
        for i in range(1, self._problem.n+1):
            for j in range(i+1, self._problem.n+1):
                if self.is_edited(i, j):
                    value += abs(self._problem.weight(i, j))
        return value

    def delta(self, add: list[(int, int)], rem: list[(int, int)]) -> int:
        df = 0
        for (u, v) in add:
            if not self._graph.connected(u, v):
                df += self._problem.weight(u, v)
        for (u, v) in rem:
            if self._graph.connected(u, v):
                df += self._problem.weight(u, v)
        return df

    def connected(self, u: int, v: int):
        return self._graph.connected(u, v)

    def is_edited(self, u: int, v: int):
        return self._problem.connected(u, v) != self._graph.connected(u, v)

    def add_edges(self, es: list[(int, int)] | set[(int, int)]):
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

    def edges(self, vs: frozenset[int] | set[int] | None = None) -> set[(int, int)]:
        return self._graph.edges(vs)

    def degree(self, v: int):
        return self._graph.degree(v)

    def neighbors(self, v: int):
        return self._graph.neighbors(v)

    def frozen_components(self):
        return self._graph.frozen_components()

    def components(self):
        return self._graph.components()

    def component(self, v: int):
        return self._graph.component(v)

    def is_feasible(self):
        for v in range(1, self._problem.n+1):
            if not self.is_vertex_feasible(v):
                # print("Not feasible anymore:", v)
                return False
        return True

    def is_vertex_feasible(self, v: int):
        c = self._graph.component(v)
        deg = self._graph.degree(v)
        return deg >= len(c) - self._problem.s

    def __repr__(self):
        return f"{self.value()}"

    def __str__(self):
        return f"{self.value()}"

    def to_file(self) -> str:
        s = StringIO()
        s.write(f"{self._problem.name}\n")
        for (u, v) in self.edges():
            if self.is_edited(u, v):
                s.write(f"{u} {v}\n")
        return s.getvalue()

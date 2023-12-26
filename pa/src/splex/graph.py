import numpy as np


class Graph:

    def __init__(self, n: int):
        self._n = n
        self._edges: set[(int, int)] = set()
        self._degrees = np.zeros(n, dtype=int)
        self._adjacent = np.zeros((n, n), dtype=bool)
        self._neighbors = {v: set() for v in range(1, n+1)}
        self._components = {v: {v} for v in range(1, n+1)}

    def connected(self, u: int, v: int) -> bool:
        return self._adjacent[u-1, v-1]

    def add_edges(self, es: list[(int, int)]):
        for (u, v) in es:
            self.add_edge(u, v)

    def add_edge(self, u: int, v: int):
        self._add_edge(u, v)
        self._degrees[u-1] += 1
        self._degrees[v-1] += 1
        self._adjacent[u-1, v-1] = True
        self._adjacent[v-1, u-1] = True
        self._neighbors[u].add(v)
        self._neighbors[v].add(u)
        self._connect_components(u, v)

    def _add_edge(self, u: int, v: int):
        m1, m2 = min(u, v), max(u, v)
        self._edges.add((m1, m2))

    def remove_edges(self, es: list[(int, int)]):
        for (u, v) in es:
            self.remove_edge(u, v)

    def remove_edge(self, u: int, v: int):
        self._remove_edge(u, v)
        self._degrees[u-1] -= 1
        self._degrees[v-1] -= 1
        self._adjacent[u-1, v-1] = False
        self._adjacent[v-1, u-1] = False
        self._neighbors[u].remove(v)
        self._neighbors[v].remove(u)
        self._disconnect_components(u, v)

    def _remove_edge(self, u: int, v: int):
        m1, m2 = min(u, v), max(u, v)
        self._edges.remove((m1, m2))

    def degree(self, v: int) -> int:
        return self._degrees[v-1]

    def neighbors(self, v: int):
        return self._neighbors[v]

    def components(self):
        l: list[set[int]] = []
        for c in self._components.values():
            if c not in l:
                l.append(c)
        return l

    def component(self, v: int):
        return self._components[v]

    def _connect_components(self, u: int, v: int):
        cu = self._components[u]
        cv = self._components[v]
        cn = cu.union(cv)
        for v in cn:
            self._components[v] = cn

    def _disconnect_components(self, u: int, v: int):
        nu = find_component(self._neighbors, u)
        nv = find_component(self._neighbors, v)
        for u in nu:
            self._components[u] = nu
        for v in nv:
            self._components[v] = nv


def find_component(ns: dict[int, set[int]], v: int):
    component: set[int] = set()
    visited = np.zeros(len(ns), dtype=bool)
    queue = [v]
    while len(queue) > 0:
        e = queue.pop()
        if not visited[e-1]:
            visited[e-1] = True
            component.add(e)
            queue.extend(ns[e])
    return component

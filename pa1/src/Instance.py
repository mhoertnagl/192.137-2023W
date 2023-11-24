from io import StringIO

import numpy as np

from DisjointSet import DisjointSet


class Instance:
    """
    Represents an s-plex problem instance.
    """

    def __init__(self, name: str, s: int, n: int, m: int):
        """
        Creates a new s-plex problem instance.
        :param name: The name of the problem instance.
        :param s: The s in s-plex.
        :param n: The number of nodes.
        :param m: The number of edges.
        """
        self.name = name
        """The name of the problem instance."""
        self.s = s
        """The s in s-plex."""
        self.n = n
        """The number of nodes."""
        self.m = m
        """The number of edges."""
        self.f = 0
        """The objective value."""
        self.__weights = np.zeros((n + 1, n + 1), dtype=int)
        """The weight matrix."""
        self.__initial_adjacency_matrix = np.zeros((n + 1, n + 1), dtype=int)
        """The initial adjacency matrix."""
        self.__current_adjacency_matrix = np.zeros((n + 1, n + 1), dtype=int)
        """The current adjacency matrix."""
        self.__change_matrix = np.zeros((n + 1, n + 1), dtype=int)
        """The edit matrix."""
        self.changeset: set[(int, int)] = set()
        """The set of edited edges."""
        # Implicit assumption: indices of vertices range from 1 to n+1.
        self.__components = Components(n)
        """The dictionary of graph components."""
        self.__connections = DisjointSet(n+1)
        """Connected vertices."""
        self.__neighbor_counts: dict[int, int] = {i+1: 0 for i in range(n)}
        """The number of neighbors for each vertex."""
        self.__edges: set[(int, int)] = set()
        """List of all edges."""
        self.__edges_by_weight: list[WeightItem] = []
        """The list of weighted edges in ascending order."""

    def add_edge(self, s: int, t: int):
        """
        Adds an edge from node s to node t and vice versa.
        and adjusts the edit status of the node.
        :param s: The start node.
        :param t: The target node.
        """
        m0, m1 = min(s, t), max(s, t)
        if self.__initial_adjacency_matrix[m0, m1] == 0:
            self.__change_matrix[m0, m1] = 1
            self.changeset.add((m0, m1))
        else:
            self.__change_matrix[m0, m1] = 0
            self.changeset.remove((m0, m1))
        self.__current_adjacency_matrix[m0, m1] = 1
        self.__components.add_edge(m0, m1)
        self.__connections.union(m0, m1)
        self.__neighbor_counts[m0] += 1
        self.__neighbor_counts[m1] += 1
        self.__edges.add((m0, m1))

    def remove_edge(self, s: int, t: int):
        """
        Removes the edge from node s to node t and vice
        versa and adjusts the edit status of the node.
        :param s: The start node.
        :param t: The target node.
        """
        m0, m1 = min(s, t), max(s, t)
        if self.__initial_adjacency_matrix[m0, m1] == 1:
            self.__change_matrix[m0, m1] = -1
            self.changeset.add((m0, m1))
        else:
            self.__change_matrix[m0, m1] = 0
            self.changeset.remove((m0, m1))
        self.__current_adjacency_matrix[m0, m1] = 0
        # TODO: Reinitialize DisjointSet.
        self.__neighbor_counts[m0] -= 1
        self.__neighbor_counts[m1] -= 1
        self.__edges.remove((m0, m1))

    def is_edited(self, s: int, t: int):
        """
        Returns True iff the edge from node s to node t
        is edited (added or removed).
        :param s: The start node.
        :param t: The target node.
        :return: True iff the edge from node s to node t
                 is edited
        """
        m0, m1 = min(s, t), max(s, t)
        return self.__change_matrix[m0, m1] == 1

    def is_adjacent(self, s: int, t: int):
        """
        Returns true iff node s is currently adjacent to
        node t.
        :param s: The start node.
        :param t: The target node.
        :return: true if s and t are adjacent, false else.
        """
        m0, m1 = min(s, t), max(s, t)
        return self.__current_adjacency_matrix[m0, m1] == 1

    def get_weight(self, s: int, t: int):
        """
        Get the weight for edge {s, t}.
        :param s: The start node.
        :param t: The target node.
        :return: The weight of edge {s, t}.
        """
        m0, m1 = min(s, t), max(s, t)
        return self.__weights[m0, m1]

    def evaluate(self):
        """
        Evaluates the objective function.
        :return: The objective value.
        """
        self.f = 0
        for i in range(self.n):
            for j in range(i+1, self.n):
                if self.__change_matrix[i + 1, j + 1] == 1:
                    self.f += self.__weights[i + 1, j + 1]
        return self.f

    def delta_evaluate(self, s: int, t: int):
        m0, m1 = min(s, t), max(s, t)
        # TODO: Check if this edge would be edited
        #       then compute delta evaluation.

    def edges(self):
        return self.__edges.__iter__()

    def edges_by_weight_ascending(self):
        return self.__edges_by_weight.__iter__()

    def __str__(self):
        s = StringIO()
        s.write(f"Name: {self.name}\n")
        s.write(f"s-plex number: {self.s}\n")
        s.write(f"Number of nodes: {self.n}\n")
        s.write(f"Number of edges: {self.m}\n")
        s.write(f"Objective value: {self.f}\n")
        s.write("Adjacency matrix A:\n")
        s.write(self.__initial_adjacency_matrix.__str__())
        s.write("\n")
        s.write("Weights matrix W:\n")
        s.write(self.__weights.__str__())
        s.write("\n")
        return s.getvalue()

    def graph(self):
        s = StringIO()
        s.write(f"graph {self.name} {{\n")
        for (v, w) in self.edges():
            s.write(f"  {v} -- {w} \n")
        s.write("}\n")
        return s.getvalue()

    def set_edge(self, s: int, t: int, p: int, w: int):
        """
        Set the adjacency and weight for nodes s and t without
        affecting the edit status of the edge.
        Call this method only to initially populate the instance.
        :param s: The start node.
        :param t: The target node.
        :param p: 0 or 1 indicating adjacency.
        :param w: The weight of edge {s, t}.
        """
        m0, m1 = min(s, t), max(s, t)
        # Set adjacency.
        if p == 1:
            self.__initial_adjacency_matrix[m0, m1] = 1
            self.__current_adjacency_matrix[m0, m1] = 1
            self.__components.add_edge(m0, m1)
            self.__connections.union(m0, m1)
            self.__neighbor_counts[m0] += 1
            self.__neighbor_counts[m1] += 1
            self.__edges.add((m0, m1))
        # Set weight.
        self.__weights[m0, m1] = w
        self.__edges_by_weight.append(WeightItem(m0, m1, w, p))

    def finish(self):
        """
        Sort the list of WeightItems. Call this
        at the end of the initial population of
        this instance.
        """
        self.evaluate()
        self.__edges_by_weight.sort()


class Components:

    def __init__(self, n: int):
        """
        Initializes with n single vertices plexes.
        :param n: The number of vertices.
        """
        self.__components: dict[int, Component] \
            = {i+1: Component(i+1) for i in range(n)}
        """The set of components."""

    def add_edge(self, i: int, j: int):
        """
        Adds an edge and connects the two components.
        :param i: First vertex of the edge.
        :param j: Second vertex of the edge.
        """
        vs = self.__components[i]
        ws = self.__components[j]
        # Add the component with fewer items to the
        # component with more items.
        if vs.n > ws.n:
            vs.union(ws)
        else:
            ws.union(vs)


class Component:

    def __init__(self, v: int):
        self.n = 1
        """The number of nodes in this component."""
        self.vertices: set[int] = set()
        """The set of nodes in this component."""
        self.vertices.add(v)

    def union(self, other):
        for v in other.vertices:
            self.vertices.add(v)
        self.n = len(self.vertices)
        other.vertices = self.vertices
        other.n = self.n


class WeightItem:

    def __init__(self, s: int, t: int, w: int, p: int):
        m0, m1 = min(s, t), max(s, t)
        self.s = m0
        """The start node."""
        self.t = m1
        """THe target node."""
        self.w = w
        """The weight."""
        self.p = p
        """The initial adjacency."""

    def __lt__(self, other):
        return self.w < other.w or (self.w == other.w and self.p > other.p)

    def __str__(self):
        return f"{self.s} {'*' if self.p == 1 else '-'}---[{self.w}]--> {self.t}"

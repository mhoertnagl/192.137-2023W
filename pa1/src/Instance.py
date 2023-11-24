from io import StringIO

import numpy as np


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
        self.__W = np.zeros((n+1, n+1), dtype=int)
        """The weight matrix."""
        self.__A = np.zeros((n+1, n+1), dtype=int)
        """The initial adjacency matrix."""
        self.__B = np.zeros((n+1, n+1), dtype=int)
        """The current adjacency matrix."""
        self.__neighbor_counts: dict[int, int] = {i+1: 0 for i in range(n)}
        """The number of neighbors for each vertex."""
        self.__E = np.zeros((n+1, n+1), dtype=int)
        """The edit matrix."""
        self.changeset: set[(int, int)] = set()
        """The set of edited edges."""
        # Implicit assumption: indices of vertices range from 1 to n+1.
        self.__P = Plexes(n)
        """The dictionary of fully connected  components."""
        self.__R: list[WeightItem] = []
        """The list of weighted edges in ascending order."""

    def add_edge(self, s: int, t: int):
        """
        Adds an edge from node s to node t and vice versa.
        and adjusts the edit status of the node.
        :param s: The start node.
        :param t: The target node.
        """
        m0, m1 = min(s, t), max(s, t)
        if self.__A[m0, m1] == 0:
            self.__E[m0, m1] = 1
            self.changeset.add((m0, m1))
        else:
            self.__E[m0, m1] = 0
            self.changeset.remove((m0, m1))
        self.__B[m0, m1] = 1
        self.__neighbor_counts[m0] += 1
        self.__neighbor_counts[m1] += 1

    def remove_edge(self, s: int, t: int):
        """
        Removes the edge from node s to node t and vice
        versa and adjusts the edit status of the node.
        :param s: The start node.
        :param t: The target node.
        """
        m0, m1 = min(s, t), max(s, t)
        if self.__A[m0, m1] == 1:
            self.__E[m0, m1] = -1
            self.changeset.add((m0, m1))
        else:
            self.__E[m0, m1] = 0
            self.changeset.remove((m0, m1))
        self.__B[m0, m1] = 0
        self.__neighbor_counts[m0] -= 1
        self.__neighbor_counts[m1] -= 1

    def is_adjacent(self, s: int, t: int):
        """
        Returns true iff node s is currently adjacent to
        node t.
        :param s: The start node.
        :param t: The target node.
        :return: true if s and t are adjacent, false else.
        """
        m0, m1 = min(s, t), max(s, t)
        return self.__B[m0, m1] == 1

    def get_weight(self, s: int, t: int):
        """
        Get the weight for edge {s, t}.
        :param s: The start node.
        :param t: The target node.
        :return: The weight of edge {s, t}.
        """
        m0, m1 = min(s, t), max(s, t)
        return self.__W[m0, m1]

    def set_weight(self, s: int, t: int, w: int):
        """
        Set the weight for edge {s, t}.
        :param s: The start node.
        :param t: The target node.
        :param w: The weight of edge {s, t}.
        """
        m0, m1 = min(s, t), max(s, t)
        self.__W[m0, m1] = w
        self.__R.append(WeightItem(m0, m1, w))

    def evaluate(self):
        """
        Evaluates the objective function.
        :return: The objective value.
        """
        self.f = 0
        for i in range(self.n):
            for j in range(i+1, self.n):
                if self.__E[i+1, j+1] == 1:
                    self.f += self.__W[i+1, j+1]
        return self.f

    def delta_evaluate(self, s: int, t: int):
        m0, m1 = min(s, t), max(s, t)
        # TODO: Check if this edge would be edited
        #       then compute delta evaluation.

    def __iter__(self):
        return self.__R.__iter__()

    def __str__(self):
        s = StringIO()
        s.write(f"Name: {self.name}\n")
        s.write(f"s-plex number: {self.s}\n")
        s.write(f"Number of nodes: {self.n}\n")
        s.write(f"Number of edges: {self.m}\n")
        s.write(f"Objective value: {self.f}\n")
        s.write("Adjacency matrix A:\n")
        s.write(self.__A.__str__())
        s.write("\n")
        s.write("Weights matrix W:\n")
        s.write(self.__W.__str__())
        s.write("\n")
        return s.getvalue()

    def set_adjacency(self, s: int, t: int, p: int):
        """
        Set the adjacency for nodes s and t without
        affecting the edit status of the edge.
        Call this method only to initially populate
        the instance.
        :param s: The start node.
        :param t: The target node.
        :param p: 0 or 1 indicating adjacency.
        """
        m0, m1 = min(s, t), max(s, t)
        self.__A[m0, m1] = p
        self.__B[m0, m1] = p
        self.__neighbor_counts[m0] += 1
        self.__neighbor_counts[m1] += 1

    def finish(self):
        """
        Sort the list of WeightItems. Call this
        at the end of the initial population of
        this instance.
        """
        self.evaluate()
        self.__R.sort()


class Plexes:

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
        vs.union(ws)


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
        # vs = self.vertices.union(other.vertices)
        # vl = len(vs)
        # self.vertices = vs
        # other.vertices = vs
        # self.n = vl
        # other.n = vl


class WeightItem:

    def __init__(self, s: int, t: int, w: int):
        m0, m1 = min(s, t), max(s, t)
        self.s = m0
        """The start node."""
        self.t = m1
        """THe target node."""
        self.w = w
        """The weight."""

    def __lt__(self, other):
        return self.w < other.w

    def __str__(self):
        return f"{self.s} ---[{self.w}]--> {self.t}"

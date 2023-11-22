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
        self.__W = np.zeros((n+1, n+1), dtype=int)
        """The weight matrix."""
        self.__A = np.zeros((n+1, n+1), dtype=int)
        """The adjacency matrix."""

    def add_edge(self, s: int, t: int):
        """
        Adds an edge from node s to node t and vice versa.
        :param s: The start node.
        :param t: The target node.
        """
        self.__A[s, t] = 1
        self.__A[t, s] = 1

    def remove_edge(self, s: int, t: int):
        """
        Removes the edge from node s to node t and vice versa.
        :param s: The start node.
        :param t: The target node.
        """
        self.__A[s, t] = 0
        self.__A[t, s] = 0

    def is_adjacent(self, s: int, t: int):
        """
        Returns true iff nodes s is adjacent to node t.
        :param s: The start node.
        :param t: The target node.
        :return: true if s and t are adjacent, false else.
        """
        return self.__A[s, t] == 1

    def set_adjacency(self, s: int, t: int, p: int):
        """
        Set the adjacency for nodes s and t.
        :param s: The start node.
        :param t: The target node.
        :param p: 0 or 1 indicating adjacency.
        """
        self.__A[s, t] = p
        self.__A[t, s] = p

    def get_weight(self, s: int, t: int):
        """
        Get the weight for edge {s, t}.
        :param s: The start node.
        :param t: The target node.
        :return: The weight of edge {s, t}.
        """
        return self.__W[s, t]

    def set_weight(self, s: int, t: int, w: int):
        """
        Set the weight for edge {s, t}.
        :param s: The start node.
        :param t: The target node.
        :param w: The weight of edge {s, t}.
        """
        self.__W[s, t] = w
        self.__W[t, s] = w

    def changes(self, b: np.ndarray):
        """
        Returns a list of edges that have been added or
        removed from the original adjacency matrix.
        :param b: Another adjacency matrix.
        :return: List of changes.
        """
        pass

    def __str__(self):
        s = StringIO()
        s.write(f"Name: {self.name}\n")
        s.write(f"s-plex number: {self.s}\n")
        s.write(f"Number of nodes: {self.n}\n")
        s.write(f"Number of edges: {self.m}\n")
        s.write("Adjacency matrix A:\n")
        s.write(self.__A.__str__())
        s.write("\n")
        s.write("Weights matrix W:\n")
        s.write(self.__W.__str__())
        s.write("\n")
        return s.getvalue()

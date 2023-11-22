from io import StringIO

import numpy as np


class Instance:
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
        self.W = np.zeros((n+1, n+1), dtype=int)
        """The weight matrix."""
        self.A = np.zeros((n+1, n+1), dtype=int)
        """The adjacency matrix."""

    def __str__(self):
        s = StringIO()
        s.write(f"Name: {self.name}\n")
        s.write(f"s-plex number: {self.s}\n")
        s.write(f"Number of nodes: {self.n}\n")
        s.write(f"Number of edges: {self.m}\n")
        s.write("Adjacency matrix A:\n")
        s.write(self.A.__str__())
        s.write("\n")
        s.write("Weights matrix W:\n")
        s.write(self.W.__str__())
        s.write("\n")
        return s.getvalue()

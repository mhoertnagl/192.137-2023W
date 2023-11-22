from io import StringIO

import numpy as np


class Instance:
    def __init__(self, s: int, n: int, m: int):
        """
        Creates a new s-plex problem instance.
        :param s: The s in s-plex.
        :param n: The number of nodes.
        :param m: The number of edges.
        """
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
        strio = StringIO()
        strio.write(f"s = {self.s}\n")
        strio.write(f"Number of nodes: {self.n}\n")
        strio.write(f"Number of edges: {self.m}\n")
        strio.write("Adjacency matrix A\n")
        strio.write(self.A.__str__())
        strio.write("\n")
        strio.write("Weights matrix W:\n")
        strio.write(self.W.__str__())
        strio.write("\n")
        return strio.getvalue()

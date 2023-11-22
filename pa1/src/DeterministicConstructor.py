import numpy as np

from Instance import Instance


class DeterministicConstructor:
    """
    Start with a fully connected adjacency matrix B.
    Iteratively consider the edge with the highest weight.
    Test whether the nodes of that edge still meet the
    s-plex criterion. If true remove the edge in B. If
    false the edge remains intact. Then continue with the
    edge with the second-highest weight.
    """

    def __init__(self, instance: Instance):
        self.__instance = instance
        """The s-plex problem instance."""
        shape = (instance.n+1, instance.n+1)
        self.__B = np.ones(shape, dtype=int)
        """The new constructed adjacency matrix."""

    def construct(self):
        pass

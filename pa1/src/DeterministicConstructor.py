import numpy as np

from Instance import Instance


class DeterministicConstructor:
    """

    """

    def __init__(self, instance: Instance):
        self.__instance = instance
        """The s-plex problem instance."""
        shape = (instance.n+1, instance.n+1)
        self.__B = np.ones(shape, dtype=int)
        """The new constructed adjacency matrix."""

    def construct(self):
        pass

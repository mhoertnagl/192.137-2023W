from abc import ABC, abstractmethod
import numpy as np

from solution import Solution


class Neighborhood(ABC):

    @abstractmethod
    def choose(self, sol: Solution) -> Solution:
        pass


class OneFlipNeighborhood(Neighborhood, ABC):

    def choose(self, sol: Solution) -> Solution:
        (i, j) = sol.random_edge_from_all()
        new_sol = sol.copy()
        new_sol.toggle_edge(i, j)
        return new_sol


class TwoExchangeNeighborhood(Neighborhood, ABC):

    def choose(self, sol: Solution) -> Solution:
        # Randomly choose component c with size >= 4.
        # Randomly choose two edges e1 = (x1, y1) and
        # e2 = (x2, y2) from c that do not share a vertex
        # (x1 != x2 != y1 != y2). There should not be
        # a direct edge between x1 and y2 or x2 and
        # y1. Or equivalently: edges (x1, y2) and
        # (x2, y1) must not exist.
        # Swap the edges.
        pass


class VertexMoveNeighborhood(Neighborhood, ABC):

    def choose(self, sol: Solution) -> Solution:
        pass

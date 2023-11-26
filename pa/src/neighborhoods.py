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
        pass


class VertexMoveNeighborhood(Neighborhood, ABC):

    def choose(self, sol: Solution) -> Solution:
        pass

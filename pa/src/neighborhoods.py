from abc import ABC, abstractmethod
import numpy as np

from solution import Solution


class Neighborhood(ABC):

    @abstractmethod
    def choose(self, solution: Solution) -> Solution:
        pass


class OneFlipNeighborhood(Neighborhood, ABC):

    def choose(self, solution: Solution) -> (Solution, int):
        e = solution.random_edge_from_all()
        new_solution = solution.copy()
        # Edges updaten
        # Delta ausrechnen


class TwoExchangeNeighborhood(Neighborhood, ABC):

    def choose(self, solution: Solution) -> Solution:
        pass


class VertexMoveNeighborhood(Neighborhood, ABC):

    def choose(self, solution: Solution) -> Solution:
        pass

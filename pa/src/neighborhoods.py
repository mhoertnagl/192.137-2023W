import random
from abc import ABC, abstractmethod
import numpy as np

from solution import Solution


class Neighborhood(ABC):

    @abstractmethod
    def choose(self, sol: Solution) -> Solution:
        pass


class OneFlipNeighborhood(Neighborhood, ABC):

    def choose(self, sol: Solution) -> Solution:
        new_sol = sol.copy()
        for (i, j) in sol.prob.all_edges:
            new_sol.toggle_edge(i, j)
            if new_sol.is_feasible():
                return new_sol
            else:
                new_sol.toggle_edge(i, j)
        # (i, j) = sol.random_edge_from_all()
        # new_sol = sol.copy()
        # new_sol.toggle_edge(i, j)
        return new_sol


class TwoExchangeNeighborhood(Neighborhood, ABC):

    def choose(self, sol: Solution) -> Solution:
        cs = sol.get_components()
        # Get components with at least two edges
        # that do not share a vertex.
        # (Ignore the shared vertex.)
        es = []  # TODO
        random.shuffle(es)
        (x1, y1) = es[0]
        (x2, y2) = es[1]
        new_sol = sol.copy()
        new_sol.remove_edge(x1, y1)
        new_sol.remove_edge(x2, y2)
        new_sol.add_edge(x1, y2)
        new_sol.add_edge(x2, y1)
        return new_sol


class VertexMoveNeighborhood(Neighborhood, ABC):

    def choose(self, sol: Solution) -> Solution:
        c1 = list(sol.get_random_component())
        c2 = list(sol.get_random_component())
        v = c1[np.random.randint(0, len(c1))]
        new_sol = sol.copy()
        # Remove edges to old component.
        for u in sol.get_neighbors(v):
            new_sol.remove_edge(u, v)
        # Add edges to new component.
        for u in c2:
            if u != v:
                new_sol.add_edge(u, v)
        return new_sol


class ComponentMergeNeighborhood(Neighborhood, ABC):

    def choose(self, sol: Solution) -> Solution:
        c1 = sol.get_random_component()
        c2 = sol.get_random_component()
        pass

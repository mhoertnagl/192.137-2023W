import random
from abc import ABC, abstractmethod
import numpy as np

from solution import Solution


class Neighborhood(ABC):

    @abstractmethod
    def choose(self, sol: Solution) -> Solution:
        pass


# class OneFlipNeighborhood(Neighborhood, ABC):
#
#     def choose(self, sol: Solution) -> Solution:
#         new_sol = sol.copy()
#         for (i, j) in sol.prob.all_edges:
#             new_sol.toggle_edge(i, j)
#             if new_sol.is_feasible():
#                 return new_sol
#         return sol


class TwoExchangeNeighborhood(Neighborhood, ABC):

    def choose(self, sol: Solution) -> Solution:
        cs = sol.get_components()
        # Consider all components of length at
        # least 4. Then the components have at
        # least 3 edges.
        cs = list(filter(lambda x: len(x) >= 4, cs))
        # Pick one of the components randomly.
        # TODO: We could do this multiple times
        #       in a single choose operation.
        c = cs[np.random.randint(0, len(cs))]
        # Get all edges for this component.
        es = sol.get_edges(c)
        # Shuffle the edges, then take the first
        # two edges.
        random.shuffle(es)
        (x1, y1) = es[0]
        (x2, y2) = es[1]
        new_sol = sol.copy()
        # Make sure that the cross-edges do not exist.
        if not sol.has_edge(x1, y2) and not sol.has_edge(x2, y1):
            # Remove the chosen edges, ...
            new_sol.remove_edge(x1, y1)
            new_sol.remove_edge(x2, y2)
            # ... then add the cross-edges.
            new_sol.add_edge(x1, y2)
            new_sol.add_edge(x2, y1)
            return new_sol
        return sol


class SingleComponentMultiExchangeNeighborhood(Neighborhood, ABC):

    def choose(self, sol: Solution) -> Solution:
        cs = sol.get_components()
        # Consider all components of length at
        # least 4. Then the components have at
        # least 3 edges.
        cs = list(filter(lambda x: len(x) >= 4, cs))
        # Pick one of the components randomly.
        # TODO: We could do this multiple times
        #       in a single choose operation.
        c = cs[np.random.randint(0, len(cs))]
        # Get all edges for this component.
        es = sol.get_edges(c)
        # Shuffle the edges, then take the first
        # two edges.
        random.shuffle(es)
        new_sol = sol.copy()
        # Iterate over all edges.
        for i in range(0, len(es)-1):
            (x1, y1) = es[i]
            (x2, y2) = es[i+1]
            # Make sure that the cross-edges do not exist.
            if not sol.has_edge(x1, y2) and not sol.has_edge(x2, y1):
                # Remove the chosen edges, ...
                new_sol.remove_edge(x1, y1)
                new_sol.remove_edge(x2, y2)
                # ... then add the cross edges.
                new_sol.add_edge(x1, y2)
                new_sol.add_edge(x2, y1)
                # Stop with the first successful exchange.
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
        cs = sol.get_components()
        if len(cs) < 2:
            return sol
        random.shuffle(cs)
        c1 = cs[0]
        c2 = cs[1]
        new_sol = sol.copy()
        for v1 in c1:
            for v2 in c2:
                new_sol.add_edge(v1, v2)
        return new_sol

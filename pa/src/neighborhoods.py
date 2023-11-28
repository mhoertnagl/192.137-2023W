import random
from abc import ABC, abstractmethod
import numpy as np

from solution import Solution


class Neighborhood(ABC):

    @abstractmethod
    def choose(self, sol: Solution) -> Solution:
        pass


class UnredundantNeighborhood(Neighborhood, ABC):

    def choose(self, sol: Solution) -> Solution:
        for c in sol.get_components():
            b = len(c) - sol.prob.s
            for u in c:
                for v in c:
                    if self.redundant(sol, b, u, v):
                        sol.remove_edge(u, v)
                    if sol.edge_deleted(u, v):
                        sol.add_edge(u, v)
        return sol

    def redundant(self, sol: Solution, b: int, u: int, v: int):
        du, dv = sol.degree(u), sol.degree(v)
        return u != v and du > b and dv > b and sol.edge_added(u, v)


class TwoFlipNeighborhood(Neighborhood, ABC):

    # first improvement
     def choose(self, sol: Solution) -> Solution:
         new_sol = sol.copy()
         for (i, j) in sol.prob.all_edges:
             for (k, l) in sol.prob.all_edges:
                 if i != k or j != l:
                     new_sol = sol.copy()
                     new_sol.toggle_edge(i, j)
                     new_sol.toggle_edge(k, l)
                 if new_sol.is_feasible():
                     if new_sol.get_value() < sol.get_value():
                         #if step_fun == "first improvement":
                         return new_sol
         return new_sol


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


class VertexSwapNeighborhood(Neighborhood, ABC):

    def choose(self, sol: Solution) -> Solution:
        c1 = list(sol.get_random_component())
        c2 = list(sol.get_random_component())
        v1 = c1[np.random.randint(0, len(c1))]
        v2 = c2[np.random.randint(0, len(c2))]
        new_sol = sol.copy()
        ns1 = list(sol.get_neighbors(v1))
        ns2 = list(sol.get_neighbors(v2))
        # Remove edges of v1 to old
        # component and add edges to v2.
        for u in ns1:
            if new_sol.has_edge(u, v1):
                new_sol.remove_edge(u, v1)
            if u != v2:
                new_sol.add_edge(u, v2)
        # Remove edges of v2 to old
        # component and add edges to v1.
        for u in ns2:
            if new_sol.has_edge(u, v2):
                new_sol.remove_edge(u, v2)
            if u != v1:
                new_sol.add_edge(u, v1)
        return new_sol


class ComponentMergeNeighborhood(Neighborhood, ABC):

    def __init__(self, k_max: int = 10):
        self.k_max = k_max

    def choose(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components() if len(c) <= self.k_max]
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

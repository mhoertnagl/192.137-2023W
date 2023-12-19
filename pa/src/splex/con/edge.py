import random
from abc import ABC

from splex import Problem, Solution
from splex.con import Construction


class EdgeConstruction(Construction, ABC):

    def __init__(self, k: int = 100):
        self.k = k

    def construct(self, problem: Problem) -> Solution:
        # edges = self.prob.initial_edges_weighted(reverse=True)
        edges = problem.all_edges_weighted(reverse=True)
        ran_edges = self.random_shuffle(edges)

        for (_, u, v) in ran_edges:
            # Find the components that contain u and v
            # respectively. Maybe the same component.
            cu = self.component(u)
            cv = self.component(v)
            # The union would be the new component if we add
            # edge (u,v).
            # Add the smaller set to the larger one.
            cn = cu.union(cv) if len(cu) > len(cv) else cv.union(cu)
            # Find the minimum degree of all vertices in the
            # unified component. For vertices u and v the degree
            # is incremented by because of the new edge added.
            min_component_degree = self.min_degree(cn, u, v)
            # Subtracting s yields the minimum required degree
            # for the unified component.
            min_required_degree = len(cn) - problem.s
            # s-plex property is met if the minimum degree of
            # unified component is greater or equal to the
            # required degree.
            if min_component_degree > min_required_degree:
                self.sol.add_edge(u, v)
                # Update the connected components.
                self.components = self.sol.get_components()
        return self.sol

    def random_shuffle(self, edges: list):
        # Partition list of edges in k long sub-lists.
        p_edges = [edges[i:i + self.k] for i in range(0, len(edges), self.k)]
        # Shuffle each sublist.
        for i in range(len(p_edges)):
            random.shuffle(p_edges[i])
            # Merge partitioned list.
        shuffled_edges = [j for i in p_edges for j in i]
        return shuffled_edges

    # Get the minimum degree node for a connected component.
    def min_degree(self, c: set, x: int, y: int) -> int:
        return min(map(lambda v: self.degree(v, x, y), c))

    # Get the degree for vertex v and the degree
    # plus one if v is x or y.
    def degree(self, v: int, x: int, y: int):
        d = self.sol.degree(v)
        return d+1 if v == x or v == y else d

    # Get the component that contains vertex v.
    def component(self, v: int) -> set:
        for c in self.components:
            if v in c:
                return c
        return set()
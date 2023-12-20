from itertools import batched, chain
from random import shuffle
from abc import ABC

from splex import Problem, Solution
from splex.con import Construction


class EdgeConstruction(Construction, ABC):

    def __init__(self, k: int = 100):
        self.k = k
        self._components: list[set[int]] = []
        self._solution = Solution()

    def construct(self, problem: Problem) -> Solution:
        self._components = [{i} for i in range(1, problem.n+1)]
        self._solution = Solution()
        for (_, u, v) in self._batch_shuffle(problem):
            # Find the components that contain u and v
            # respectively. Maybe the same component.
            cu = self._component(u)
            cv = self._component(v)
            # The union would be the new component if we add
            # edge (u,v).
            # Add the smaller set to the larger one.
            cn = cu.union(cv) if len(cu) > len(cv) else cv.union(cu)
            # Find the minimum degree of all vertices in the
            # unified component. For vertices u and v the degree
            # is incremented by because of the new edge added.
            min_component_degree = self._min_degree(cn, u, v)
            # Subtracting s yields the minimum required degree
            # for the unified component.
            min_required_degree = len(cn) - problem.s
            # s-plex property is met if the minimum degree of
            # unified component is greater to the required degree.
            if min_component_degree > min_required_degree:
                self._solution.add_edge(u, v)
                # Update the connected components.
                self._components = self._solution.get_components()
        return self._solution

    def _batch_shuffle(self, problem: Problem):
        batches = batched(problem.all_edges(), self.k)
        for batch in batches:
            shuffle(batch)
        return list(chain.from_iterable(batches))

    # Get the minimum degree node for a connected component.
    def _min_degree(self, c: set, x: int, y: int) -> int:
        return min(map(lambda v: self._degree(v, x, y), c))

    # Get the degree for vertex v and the degree
    # plus one if v is x or y.
    def _degree(self, v: int, x: int, y: int):
        d = self._solution.degree(v)
        return d+1 if v == x or v == y else d

    # Get the component that contains vertex v.
    def _component(self, v: int) -> set[int]:
        for c in self._components:
            if v in c:
                return c
        return set()

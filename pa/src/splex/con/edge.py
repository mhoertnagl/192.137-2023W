# from itertools import batched, chain
from random import shuffle
from abc import ABC

from splex import Problem, Solution
from splex.con import Construction


class EdgeConstruction(Construction, ABC):

    def __init__(self, k: int = 100):
        self._k = k

    def construct(self, problem: Problem) -> Solution:
        solution = Solution(problem)
        for (_, u, v) in self._batch_shuffle(problem):
            # Find the components that contain u and v
            # respectively. Maybe the same component.
            cu = solution.component(u)
            cv = solution.component(v)
            # The union would be the new component if we add
            # edge (u,v).
            # # Add the smaller set to the larger one.
            cn = cu.union(cv) # if len(cu) > len(cv) else cv.union(cu)
            # Find the minimum degree of all vertices in the
            # unified component. For vertices u and v the degree
            # is incremented by because of the new edge added.
            min_component_degree = self._min_degree(solution, cn, u, v)
            # Subtracting s yields the minimum required degree
            # for the unified component.
            min_required_degree = len(cn) - problem.s
            # s-plex property is met if the minimum degree of
            # unified component is greater to the required degree.
            if min_component_degree > min_required_degree:
                solution.add_edge(u, v)
        return solution

    # def _batch_shuffle(self, problem: Problem):
    #     batches = batched(problem.all_edges(), self.k)
    #     for batch in batches:
    #         shuffle(batch)
    #     return list(chain.from_iterable(batches))

    def _batch_shuffle(self, problem: Problem):
        # Partition list of edges in k long sub-lists.
        edges = problem.all_edges()
        p_edges = [edges[i:i + self._k] for i in range(0, len(edges), self._k)]
        # Shuffle each sublist.
        for i in range(len(p_edges)):
            shuffle(p_edges[i])
        # Merge partitioned list.
        return [j for i in p_edges for j in i]

    # Get the minimum degree node for a connected component.
    def _min_degree(self, s: Solution, c: set, x: int, y: int) -> int:
        return min(map(lambda v: self._degree(s, v, x, y), c))

    # Get the degree for vertex v and the degree
    # plus one if v is x or y.
    def _degree(self, s: Solution, v: int, x: int, y: int):
        deg = s.degree(v)
        return deg+1 if v == x or v == y else deg

    def __repr__(self):
        return f"Edge Construction [k={self._k}]"

    def __str__(self):
        return self.__repr__()

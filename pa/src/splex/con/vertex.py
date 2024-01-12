import random
from abc import ABC

from .construction import Construction
from splex import Problem, Solution


class VertexConstruction(Construction, ABC):

    def construct(self, problem: Problem) -> Solution:
        solution = Solution(problem)
        vertices = list(range(1, problem.n+1))
        random.shuffle(vertices)
        for v in vertices:
            best_e, best_d = None, 0
            for c in solution.components():
                if v not in c:
                    cv = solution.component(v)
                    edges = [(u, w) for u in c for w in cv]
                    delta = solution.delta(edges, [])
                    if delta < best_d:
                        best_e = edges
                        best_d = delta
            if best_d < 0:
                solution.add_edges(best_e)
        return solution

    def __repr__(self):
        return f"Vertex Construction"

    def __str__(self):
        return self.__repr__()

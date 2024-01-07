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
            best_e, best_d = None, None
            for c in solution.components():
                if v not in c:
                    edges, delta = find_edges_to_add(solution, v, c)
                    if best_d is None or delta < best_d:
                        best_e = edges
                        best_d = delta
            if best_e is not None:
                solution.add_edges(best_e)
        return solution


def find_edges_to_add(sol: Solution, v: int, c: set[int]):
    edges = []
    for u in c:
        edges.append((u, v))
    return edges, sol.delta(edges, [])

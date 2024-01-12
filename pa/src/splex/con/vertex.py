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
                    if best_d is None or delta < best_d:
                        best_e = edges
                        best_d = delta
            if best_d < 0:
                solution.add_edges(best_e)
        return solution

    def __repr__(self):
        return f"Vertex Construction"

    def __str__(self):
        return self.__repr__()


# class VertexConstruction(Construction, ABC):
#
#     def construct(self, problem: Problem) -> Solution:
#         solution = Solution(problem)
#         vertices = list(range(1, problem.n+1))
#         random.shuffle(vertices)
#         for v in vertices:
#             feasible = solution.is_feasible()
#             best_e, best_d = None, None
#             for c in solution.components():
#                 if v not in c:
#                     edges = [(u, v) for u in c]
#                     delta = solution.delta(edges, [])
#                     if best_d is None or delta < best_d:
#                         best_e = edges
#                         best_d = delta
#             if best_e is not None:
#                 solution.add_edges(best_e)
#         return solution
#
#     def __repr__(self):
#         return f"Vertex Construction"
#
#     def __str__(self):
#         return self.__repr__()


class VertexConstruction2(Construction, ABC):

    def construct(self, problem: Problem) -> Solution:
        solution = Solution(problem)
        vertices = list(range(1, problem.n+1))
        random.shuffle(vertices)
        for v in vertices:
            best_e, best_d = None, None
            for c in solution.components():
                if v not in c:
                    edges, delta = find_edges_to_add2(problem, solution, v, c)
                    if best_d is None or delta < best_d:
                        best_e = edges
                        best_d = delta
            if best_e is not None:
                solution.add_edges(best_e)
        return solution

    def __repr__(self):
        return f"Vertex Construction 2"

    def __str__(self):
        return self.__repr__()


def find_edges_to_add2(prob: Problem, sol: Solution, v: int, c: set[int]):
    edges = []
    for u in c:
        edges.append((u, v))
    if len(c) > prob.s + 1:
        wedges = prob.weights_for_edges(edges)
        edges = [(u, v) for (w, u, v) in wedges[:len(c)+1-prob.s]]
    return edges, sol.delta(edges, [])

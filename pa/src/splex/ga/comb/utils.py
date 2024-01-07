from abc import ABC
from random import shuffle

from splex import Problem, Solution
from splex.ga.population import Population
from splex.ga.comb import Combiner


# class ComponentsCombiner(Combiner, ABC):
#
#     def recombine(self,
#                   problem: Problem,
#                   selected: Population) -> Population:
#         kids: list[Solution] = []
#         for i in range(len(selected)):
#             parent1 = selected[i]
#             components1 = parent1.frozen_components()
#             for j in range(i+1, len(selected)):
#                 parent2 = selected[j]
#                 components2 = parent2.frozen_components()
#                 solution = Solution(problem)
#                 # Add all components that both parents have in common.
#                 common = components2.intersection(components1)
#                 for component in common:
#                     # TODO: Pick component edges with lower value?
#                     edges = parent2.edges(component)
#                     solution.add_edges(edges)
#                 # This Operation is not clearly defined
#                 remain1 = components1.difference(common)
#                 remain2 = components2.difference(common)
#                 remain = list(components2.symmetric_difference(components1))
#                 shuffle(remain)
#                 choice, missing = select_components(remain)
#                 for component in choice:
#                     pass
#                 # Common components
#                 # Remaining components
#                 # Create graph (Solution) from components.
#                 # How to combine the mismatching components.
#                 kids.append(solution)
#         return Population(kids)


def select_components(components: list[frozenset[int]]):
    included: set[int] = set()  # Vertices already contained in the result set.
    universe: set[int] = set()  # All vertices in all components.
    result: set[frozenset[int]] = set()
    for component in components:
        common = included.intersection(component)
        if len(common) == 0:
            result.add(component)
            included = included.union(component)
        universe = universe.union(component)
    excluded = universe.difference(included)
    return result, excluded


def pick_components(cs1: list[frozenset[int]], cs2: list[frozenset[int]]):
    included: set[int] = set()  # Vertices already contained in the result sets.
    universe: set[int] = set()  # All vertices in all components.
    rs1: set[frozenset[int]] = set()
    rs2: set[frozenset[int]] = set()
    for i in range(max(len(cs1), len(cs2))):
        if i < len(cs1):
            c1 = cs1[i]
            if len(included.intersection(c1)) == 0:
                rs1.add(c1)
                included = included.union(c1)
            universe = universe.union(c1)
        if i < len(cs2):
            c2 = cs2[i]
            if len(included.intersection(c2)) == 0:
                rs2.add(c2)
                included = included.union(c2)
            universe = universe.union(c2)
    excluded = universe.difference(included)
    return rs1, rs2, excluded


def merge_parents(problem: Problem, p1: Solution, p2: Solution):
    kid = Solution(problem)
    cs1 = list(p1.frozen_components())
    cs2 = list(p2.frozen_components())
    shuffle(cs1)
    shuffle(cs2)
    rs1, rs2, _ = pick_components(cs1, cs2)
    for c1 in rs1:
        kid.add_edges(p1.edges(c1))
    for c2 in rs2:
        kid.add_edges(p2.edges(c2))
    return kid

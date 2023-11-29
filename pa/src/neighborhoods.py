import random
from abc import ABC, abstractmethod
from enum import Enum

import numpy as np

from solution import Solution


class Improvement(Enum):
    RANDOM = 1
    FIRST = 2
    BEST = 3


class Neighborhood(ABC):

    def __init__(self, improve: Improvement = Improvement.RANDOM):
        self.improve = improve

    def choose(self, sol: Solution) -> Solution:
        match self.improve:
            case Improvement.RANDOM:
                return self.choose_random(sol)
            case Improvement.FIRST:
                return self.choose_first(sol)
            case Improvement.BEST:
                return self.choose_best(sol)
        return sol

    @abstractmethod
    def choose_random(self, sol: Solution) -> Solution:
        pass

    @abstractmethod
    def choose_first(self, sol: Solution) -> Solution:
        pass

    @abstractmethod
    def choose_best(self, sol: Solution) -> Solution:
        pass


class TwoFlipNeighborhood(Neighborhood, ABC):

    def __init__(self, improve: Improvement = Improvement.RANDOM):
        super().__init__(improve)
        self.improve = improve

    def choose_random(self, sol: Solution) -> Solution:
        new_sol = sol.copy()
        edges = sol.prob.all_edges
        random.shuffle(edges)
        (i, j), (k, l) = edges[0], edges[1]
        new_sol.toggle_edge(i, j)
        new_sol.toggle_edge(k, l)
        return new_sol if new_sol.is_feasible() else sol

    def choose_first(self, sol: Solution) -> Solution:
        edges = sol.prob.all_edges_weighted()
        for x in range(0, len(edges)):
            for y in range(x+1, len(edges)):
                (_, i, j), (_, k, l) = edges[x], edges[y]
                new_sol = sol.copy()
                new_sol.toggle_edge(i, j)
                new_sol.toggle_edge(k, l)
                if new_sol.is_feasible():
                    if new_sol.get_value() < sol.get_value():
                        return new_sol
        return sol

    def choose_best(self, sol: Solution) -> Solution:
        edges = sol.prob.all_edges_weighted()
        for x in range(0, len(edges)):
            for y in range(x+1, len(edges)):
                (_, i, j), (_, k, l) = edges[x], edges[y]
                new_sol = sol.copy()
                new_sol.toggle_edge(i, j)
                new_sol.toggle_edge(k, l)
                if new_sol.is_feasible():
                    if new_sol.get_value() < sol.get_value():
                        sol = new_sol
        return sol


class TwoExchangeNeighborhood(Neighborhood, ABC):

    def __init__(self, improve: Improvement = Improvement.RANDOM):
        super().__init__(improve)
        self.improve = improve

    def choose_random(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components() if len(c) >= 4]
        if len(cs) < 1:
            return  sol
        c = cs[np.random.randint(0, len(cs))]
        es = sol.get_edges(c)
        random.shuffle(es)
        (x1, y1), (x2, y2) = es[0], es[1]
        new_sol = sol.copy()
        if not sol.has_edge(x1, y2) and not sol.has_edge(x2, y1):
            new_sol.remove_edge(x1, y1)
            new_sol.remove_edge(x2, y2)
            new_sol.add_edge(x1, y2)
            new_sol.add_edge(x2, y1)
            return new_sol
        return sol

    def choose_first(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components() if len(c) >= 4]
        for c in cs:
            es = sol.get_edges(c)
            for x in range(0, len(es)):
                for y in range(x+1, len(es)):
                    (x1, y1), (x2, y2) = es[x], es[y]
                    new_sol = sol.copy()
                    if not sol.has_edge(x1, y2) and not sol.has_edge(x2, y1):
                        new_sol.remove_edge(x1, y1)
                        new_sol.remove_edge(x2, y2)
                        new_sol.add_edge(x1, y2)
                        new_sol.add_edge(x2, y1)
                        if new_sol.get_value() < sol.get_value():
                            return new_sol
        return sol

    def choose_best(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components() if len(c) >= 4]
        for c in cs:
            es = sol.get_edges(c)
            for x in range(0, len(es)):
                for y in range(x+1, len(es)):
                    (x1, y1), (x2, y2) = es[x], es[y]
                    new_sol = sol.copy()
                    if not sol.has_edge(x1, y2) and not sol.has_edge(x2, y1):
                        new_sol.remove_edge(x1, y1)
                        new_sol.remove_edge(x2, y2)
                        new_sol.add_edge(x1, y2)
                        new_sol.add_edge(x2, y1)
                        if new_sol.get_value() < sol.get_value():
                            sol = new_sol
        return sol


class VertexMoveNeighborhood(Neighborhood, ABC):

    def __init__(self, improve: Improvement = Improvement.RANDOM):
        super().__init__(improve)
        self.improve = improve

    def choose_random(self, sol: Solution) -> Solution:
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

    def choose_first(self, sol: Solution) -> Solution:
        cs = [list(c) for c in sol.get_components()]
        for x in range(0, len(cs)):
            for y in range(x+1, len(cs)):
                c1, c2 = cs[x], cs[y]
                for v in c1:
                    new_sol = sol.copy()
                    for u in sol.get_neighbors(v):
                        new_sol.remove_edge(u, v)
                    # smart adding of vertices
                    weighted_edges = sol.get_edges_weighted(v, c2)
                    cheap_edges = weighted_edges[:len(c2)+1-sol.prob.s]
                    exp_edges = weighted_edges[-(sol.prob.s -1):]
                    for u in cheap_edges:
                        if u != v:
                            new_sol.add_edge(u, v)
                    for u in exp_edges:                        
                        if not new_sol.is_vertex_feasible(u):
                            weighted_edges = sol.get_edges_weighted(u, cheap_edges)
                            new_sol.add_edge(u, weighted_edges[0])                        
                    if new_sol.get_value() < sol.get_value():
                        return new_sol
        return sol

    def choose_best(self, sol: Solution) -> Solution:
        cs = [list(c) for c in sol.get_components()]
        for x in range(0, len(cs)):
            for y in range(x+1, len(cs)):
                c1, c2 = cs[x], cs[y]
                for v in c1:
                    new_sol = sol.copy()
                    for u in sol.get_neighbors(v):
                        new_sol.remove_edge(u, v)
                    for u in c2:
                        if u != v:
                            new_sol.add_edge(u, v)
                    if new_sol.get_value() < sol.get_value():
                        sol = new_sol
        return sol


class VertexSwapNeighborhood(Neighborhood, ABC):

    def __init__(self, improve: Improvement = Improvement.RANDOM):
        super().__init__(improve)
        self.improve = improve

    def choose_random(self, sol: Solution) -> Solution:
        c1 = list(sol.get_random_component())
        c2 = list(sol.get_random_component())
        v1 = c1[np.random.randint(0, len(c1))]
        v2 = c2[np.random.randint(0, len(c2))]
        new_sol = sol.copy()
        ns1 = list(sol.get_neighbors(v1))
        ns2 = list(sol.get_neighbors(v2))
        for u in ns1:
            if new_sol.has_edge(u, v1):
                new_sol.remove_edge(u, v1)
            if u != v2:
                new_sol.add_edge(u, v2)
        for u in ns2:
            if new_sol.has_edge(u, v2):
                new_sol.remove_edge(u, v2)
            if u != v1:
                new_sol.add_edge(u, v1)
        return new_sol

    def choose_first(self, sol: Solution) -> Solution:
        cs = [list(c) for c in sol.get_components()]
        for x in range(0, len(cs)):
            for y in range(x+1, len(cs)):
                c1, c2 = cs[x], cs[y]
                for v1 in c1:
                    for v2 in c2:
                        new_sol = sol.copy()
                        ns1 = list(sol.get_neighbors(v1))
                        ns2 = list(sol.get_neighbors(v2))
                        for u in ns1:
                            if new_sol.has_edge(u, v1):
                                new_sol.remove_edge(u, v1)
                            if u != v2:
                                new_sol.add_edge(u, v2)
                        for u in ns2:
                            if new_sol.has_edge(u, v2):
                                new_sol.remove_edge(u, v2)
                            if u != v1:
                                new_sol.add_edge(u, v1)
                        if new_sol.get_value() < sol.get_value():
                            return new_sol
        return sol

    def choose_best(self, sol: Solution) -> Solution:
        cs = [list(c) for c in sol.get_components()]
        for x in range(0, len(cs)):
            for y in range(x+1, len(cs)):
                c1, c2 = cs[x], cs[y]
                for v1 in c1:
                    for v2 in c2:
                        new_sol = sol.copy()
                        ns1 = list(sol.get_neighbors(v1))
                        ns2 = list(sol.get_neighbors(v2))
                        for u in ns1:
                            if new_sol.has_edge(u, v1):
                                new_sol.remove_edge(u, v1)
                            if u != v2:
                                new_sol.add_edge(u, v2)
                        for u in ns2:
                            if new_sol.has_edge(u, v2):
                                new_sol.remove_edge(u, v2)
                            if u != v1:
                                new_sol.add_edge(u, v1)
                        if new_sol.get_value() < sol.get_value():
                            sol = new_sol
        return sol


class ComponentMergeNeighborhood(Neighborhood, ABC):

    def __init__(self, improve: Improvement = Improvement.RANDOM, k_max: int = 10):
        super().__init__(improve)
        self.improve = improve
        self.k_max = k_max

    def choose_random(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components() if len(c) <= self.k_max]
        if len(cs) < 2:
            return sol
        random.shuffle(cs)
        c1, c2 = cs[0], cs[1]
        new_sol = sol.copy()
        for v1 in c1:
            for v2 in c2:
                new_sol.add_edge(v1, v2)
        return new_sol

    def choose_first(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components() if len(c) <= self.k_max]
        if len(cs) < 2:
            return sol
        for x in range(0, len(cs)):
            for y in range(x+1, len(cs)):
                c1, c2 = cs[x], cs[y]
                new_sol = sol.copy()
                for v1 in c1:
                    for v2 in c2:
                        new_sol.add_edge(v1, v2)
                if new_sol.get_value() < sol.get_value():
                    return new_sol
        return sol

    def choose_best(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components() if len(c) <= self.k_max]
        if len(cs) < 2:
            return sol
        for x in range(0, len(cs)):
            for y in range(x+1, len(cs)):
                c1, c2 = cs[x], cs[y]
                new_sol = sol.copy()
                for v1 in c1:
                    for v2 in c2:
                        new_sol.add_edge(v1, v2)
                if new_sol.get_value() < sol.get_value():
                    sol = new_sol
        return sol


class RandomUnionNeighborhood(Neighborhood, ABC):

    def __init__(self, improve: Improvement = Improvement.RANDOM, k_max: int = 10):
        super().__init__(improve)
        self.nbhs = [
            ComponentMergeNeighborhood(improve, k_max),
            VertexMoveNeighborhood(improve),
            TwoFlipNeighborhood(improve),
        ]
        self.improve = improve
        self.k_max = k_max

    def choose_random(self, sol: Solution) -> Solution:
        random.shuffle(self.nbhs)
        return self.nbhs[0].choose(sol)

    def choose_first(self, sol: Solution) -> Solution:
        random.shuffle(self.nbhs)
        return self.nbhs[0].choose(sol)

    def choose_best(self, sol: Solution) -> Solution:
        random.shuffle(self.nbhs)
        return self.nbhs[0].choose(sol)

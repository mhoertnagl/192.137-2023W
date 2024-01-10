import random
from abc import ABC, abstractmethod
from enum import Enum
from milp_model import MILPModel
from milp_model_fast import MILPModelFast

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


class OneFlipNeighborhood(Neighborhood, ABC):

    def __init__(self, improve: Improvement = Improvement.RANDOM):
        super().__init__(improve)
        self.improve = improve

    def choose_random(self, sol: Solution) -> Solution:
        edges = sol.prob.all_edges
        (u, v) = edges[np.random.randint(0, len(edges))]
        sol.toggle_edge(u, v)
        if not sol.is_feasible():
            sol.toggle_edge(u, v)
        return sol

    def choose_first(self, sol: Solution) -> Solution:
        edges = sol.prob.all_edges_weighted()
        for x in range(0, len(edges)):
            (_, i, j)= edges[x]
            new_sol = sol.copy()
            new_sol.toggle_edge(i, j)
            if new_sol.is_feasible():
                    if new_sol.get_value() < sol.get_value():
                        return new_sol
        return sol

    def choose_best(self, sol: Solution) -> Solution:
        new_sol = sol.copy()
        edges = sol.prob.all_edges_weighted()
        for x in range(0, len(edges)):
            (_, i, j)= edges[x]
            test_sol = sol.copy()
            test_sol.toggle_edge(i, j)
            if test_sol.is_feasible():
                    if test_sol.get_value() < new_sol.get_value():
                        new_sol = test_sol.copy()
        return new_sol


class TwoFlipNeighborhood(Neighborhood, ABC):

    def __init__(self, improve: Improvement = Improvement.RANDOM):
        super().__init__(improve)
        self.improve = improve

    def choose_random(self, sol: Solution) -> Solution:
        edges = sol.prob.all_edges
        random.shuffle(edges)
        (i, j), (k, l) = edges[0], edges[1]
        sol.toggle_edge(i, j)
        sol.toggle_edge(k, l)
        if not sol.is_feasible():
            sol.toggle_edge(i, j)
            sol.toggle_edge(k, l)
        return sol

    def choose_first(self, sol: Solution) -> Solution:
        edges = sol.prob.all_edges_weighted()
        for x in range(0, len(edges)):
            for y in range(x+1, len(edges)):
                (_, i, j), (_, k, l) = edges[x], edges[y]
                prev_f = sol.get_value()
                sol.toggle_edge(i, j)
                sol.toggle_edge(k, l)
                if sol.is_feasible() and (sol.get_value() < prev_f):
                    return sol
                sol.toggle_edge(i, j)
                sol.toggle_edge(k, l)
        return sol

    def choose_best(self, sol: Solution) -> Solution:
        edges = sol.prob.all_edges_weighted()
        best, best_f = None, 0
        for x in range(0, len(edges)):
            for y in range(x+1, len(edges)):
                (_, i, j), (_, k, l) = edges[x], edges[y]
                sol.toggle_edge(i, j)
                sol.toggle_edge(k, l)
                new_f = sol.get_value()
                if sol.is_feasible() and (best is None or new_f < best_f):
                    best, best_f = [(i, j), (k, l)], new_f
                sol.toggle_edge(i, j)
                sol.toggle_edge(k, l)
        if best is not None:
            [(i, j), (k, l)] = best
            sol.toggle_edge(i, j)
            sol.toggle_edge(k, l)
        return sol


class TwoExchangeNeighborhood(Neighborhood, ABC):

    def __init__(self, improve: Improvement = Improvement.RANDOM):
        super().__init__(improve)
        self.improve = improve

    def choose_random(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components() if len(c) >= 4]
        if len(cs) < 1:
            return sol
        c = cs[np.random.randint(0, len(cs))]
        es = sol.get_edges(c)
        random.shuffle(es)
        (x1, y1), (x2, y2) = es[0], es[1]
        if not sol.has_edge(x1, y2) and not sol.has_edge(x2, y1):
            sol.remove_edge(x1, y1)
            sol.remove_edge(x2, y2)
            sol.add_edge(x1, y2)
            sol.add_edge(x2, y1)
        return sol

    def choose_first(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components() if len(c) >= 4]
        for c in cs:
            es = sol.get_edges(c)
            for x in range(len(es)):
                for y in range(x+1, len(es)):
                    (x1, y1), (x2, y2) = es[x], es[y]
                    if not sol.has_edge(x1, y2) and not sol.has_edge(x2, y1):
                        add = [(x1, y2), (x2, y1)]
                        rem = [(x1, y1), (x2, y2)]
                        df = sol.delta(add, rem)
                        if df < 0:
                            sol.remove_edges(rem)
                            sol.add_edges(add)
                            return sol
        return sol

    def choose_best(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components() if len(c) >= 4]
        best, best_df = None, 0
        for c in cs:
            es = sol.get_edges(c)
            for x in range(len(es)):
                for y in range(x+1, len(es)):
                    (x1, y1), (x2, y2) = es[x], es[y]
                    if not sol.has_edge(x1, y2) and not sol.has_edge(x2, y1):
                        add = [(x1, y2), (x2, y1)]
                        rem = [(x1, y1), (x2, y2)]
                        df = sol.delta(add, rem)
                        if best is None or df < best_df:
                            best, best_df = (add, rem), df
        if best is not None:
            (add, rem) = best
            sol.remove_edges(rem)
            sol.add_edges(add)
        return sol

class MILPVertexMoveNeighborhoodFast(Neighborhood, ABC):

    def __init__(self,
                 improve: Improvement = Improvement.RANDOM,
                 k_max: int = 5, time_limit: int = 60):
        super().__init__(improve)
        self.improve = improve
        self.k_max = k_max
        self.time_limit = time_limit

    def choose_random(self, sol: Solution) -> Solution:
        cs = sol.get_components()
        if len(cs) < 2:
            return sol
        random.shuffle(cs)
        c1 = list(cs[0])
        c2 = list(cs[1])
        
        v = c1[np.random.randint(0, len(c1))]
        rem = [(u, v) for u in sol.get_neighbors(v)]
        add = [u for u in c2 if u != v]
        add.append(v)
        # df = sol.delta(add, rem)
        # if df < 0:
        sol.remove_edges(rem)
        milp_model = MILPModelFast(sol, add)
        sol, A_solved = milp_model.solve(time_limit=self.time_limit)
        return sol

    def choose_first(self, sol: Solution) -> Solution:
        cs = sol.get_components()
        f = sol.get_value()
        if len(cs) < 2:
            return sol
        random.shuffle(cs)
        r = range(len(cs))
        for c1, c2 in ((cs[x], cs[y]) for x in r
                                      for y in r if x != y):
            for v in c1:
                rem = [(u, v) for u in sol.get_neighbors(v)]
                add = [u for u in c2 if u != v]
                add.append(v)
                sol.remove_edges(rem)
                milp_model = MILPModelFast(sol.copy(), add)
                sol_new, A_solved = milp_model.solve(time_limit=self.time_limit)
                sol_new, A_solved = milp_model.solve()
                df = sol_new.get_value()
                if df < f:
                    return sol_new
                else:
                    sol.add_edges(rem)
        return sol

    def choose_best(self, sol: Solution) -> Solution:
        cs = sol.get_components()
        r = range(len(cs))
        best, best_df = None, 0
        for c1, c2 in ((cs[x], cs[y]) for x in r
                                      for y in r if x != y):
            for v in c1:
                rem = [(u, v) for u in sol.get_neighbors(v)]
                add = [(u, v) for u in c2 if u != v]
                df = sol.delta(add, rem)
                if best is None or df < best_df:
                    best, best_df = (add, rem), df
        if best is not None:
            (add, rem) = best
            sol.remove_edges(rem)
            sol.add_edges(add)
        return sol

class VertexMoveNeighborhood(Neighborhood, ABC):

    def __init__(self, improve: Improvement = Improvement.RANDOM):
        super().__init__(improve)
        self.improve = improve

    def choose_random(self, sol: Solution) -> Solution:
        c1 = list(sol.get_random_component())
        c2 = list(sol.get_random_component())
        v = c1[np.random.randint(0, len(c1))]
        rem = [(u, v) for u in sol.get_neighbors(v)]
        add = [(u, v) for u in c2 if u != v]
        # df = sol.delta(add, rem)
        # if df < 0:
        sol.remove_edges(rem)
        sol.add_edges(add)
        return sol

    def choose_first(self, sol: Solution) -> Solution:
        cs = sol.get_components()
        r = range(len(cs))
        for c1, c2 in ((cs[x], cs[y]) for x in r
                                      for y in r if x != y):
            for v in c1:
                rem = [(u, v) for u in sol.get_neighbors(v)]
                add = [(u, v) for u in c2 if u != v]
                df = sol.delta(add, rem)
                if df < 0:
                    sol.remove_edges(rem)
                    sol.add_edges(add)
                    return sol
        return sol

    def choose_best(self, sol: Solution) -> Solution:
        cs = sol.get_components()
        r = range(len(cs))
        best, best_df = None, 0
        for c1, c2 in ((cs[x], cs[y]) for x in r
                                      for y in r if x != y):
            for v in c1:
                rem = [(u, v) for u in sol.get_neighbors(v)]
                add = [(u, v) for u in c2 if u != v]
                df = sol.delta(add, rem)
                if best is None or df < best_df:
                    best, best_df = (add, rem), df
        if best is not None:
            (add, rem) = best
            sol.remove_edges(rem)
            sol.add_edges(add)
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
        rem1 = [(u, v1) for u in sol.get_neighbors(v1)]
        add1 = [(u, v1) for u in sol.get_neighbors(v2)]
        rem2 = [(u, v2) for u in sol.get_neighbors(v2)]
        add2 = [(u, v2) for u in sol.get_neighbors(v1)]
        add = add1 + add2
        rem = rem1 + rem2
        df = sol.delta(add, rem)
        if df < 0:
            sol.remove_edges(rem)
            sol.add_edges(add)
        return sol

    def choose_first(self, sol: Solution) -> Solution:
        cs = sol.get_components()
        random.shuffle(cs)
        for c1, c2 in ((cs[x], cs[y]) for x in range(len(cs))
                                      for y in range(x+1, len(cs))):
            for u, v in ((u, v) for u in c1 for v in c2):
                rem1 = [(w, u) for w in sol.get_neighbors(u)]
                add1 = [(w, u) for w in sol.get_neighbors(v)]
                rem2 = [(w, v) for w in sol.get_neighbors(v)]
                add2 = [(w, v) for w in sol.get_neighbors(u)]
                df = sol.delta(add1 + add2, rem1 + rem2)
                if df < 0:
                    sol.remove_edges(rem1)
                    sol.add_edges(add1)
                    sol.remove_edges(rem2)
                    sol.add_edges(add2)
                    return sol
        return sol

    def choose_best(self, sol: Solution) -> Solution:
        cs = sol.get_components()
        best, best_df = None, 0
        for c1, c2 in ((cs[x], cs[y]) for x in range(len(cs))
                                      for y in range(x+1, len(cs))):
            for u, v in ((u, v) for u in c1 for v in c2):
                rem1 = [(w, u) for w in sol.get_neighbors(u)]
                add1 = [(w, u) for w in sol.get_neighbors(v)]
                rem2 = [(w, v) for w in sol.get_neighbors(v)]
                add2 = [(w, v) for w in sol.get_neighbors(u)]
                add, rem = add1 + add2, rem1 + rem2
                df = sol.delta(add, rem)
                if best is None or df < best_df:
                    best, best_df = (add, rem), df
        if best is not None:
            (add, rem) = best
            sol.remove_edges(rem)
            sol.add_edges(add)
        return sol


class ComponentMergeNeighborhood(Neighborhood, ABC):

    def __init__(self,
                 improve: Improvement = Improvement.RANDOM,
                 k_max: int = 10):
        super().__init__(improve)
        self.improve = improve
        self.k_max = k_max

    def choose_random(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components() if len(c) <= self.k_max]
        if len(cs) < 2:
            return sol
        random.shuffle(cs)
        
        add = sol.get_edges_between(cs[0], cs[1])
        # df = sol.delta(add, [])
        # if df < 0:
        sol.add_edges(add)
        return sol

    def choose_first(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components()
                      if len(c) <= self.k_max]
        if len(cs) < 2:
            return sol
        random.shuffle(cs)
        for c1, c2 in ((cs[x], cs[y]) for x in range(len(cs))
                                      for y in range(x+1, len(cs))):
            add = sol.get_edges_between(c1, c2)
            df = sol.delta(add, [])
            if df < 0:
                sol.add_edges(add)
                return sol
        return sol

    def choose_best(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components()
                      if len(c) <= self.k_max]
        if len(cs) < 2:
            return sol
        best, best_df = None, 0
        for c1, c2 in ((cs[x], cs[y]) for x in range(len(cs))
                                      for y in range(x+1, len(cs))):
            add = sol.get_edges_between(c1, c2)
            df = sol.delta(add, [])
            if best is None or df < best_df:
                best, best_df = add, df
        if best is not None:
            sol.add_edges(best)
        return sol

class MILPMergeComponents(Neighborhood, ABC):

    def __init__(self,
                 improve: Improvement = Improvement.RANDOM,
                 k_max: int = 5, time_limit: int = 60):
        super().__init__(improve)
        self.improve = improve
        self.k_max = k_max
        self.time_limit = time_limit

    def choose_random(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components() if len(c) <= self.k_max]
        if len(cs) < 2:
            return sol
        random.shuffle(cs)                 
        milp_model = MILPModel(sol,cs[0].union(cs[1]))
        sol, A_solved = milp_model.solve(self.time_limit,False)        
        return sol

    def choose_first(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components()
                      if len(c) <= self.k_max]
        if len(cs) < 2:
            return sol
        random.shuffle(cs)
        for c1, c2 in ((cs[x], cs[y]) for x in range(len(cs))
                                      for y in range(x+1, len(cs))):
            f = sol.get_value()
            sol_new = sol.copy()
            milp_model = MILPModel(sol_new,c1.union(c2))
            sol_new, A_solved = milp_model.solve(self.time_limit,False)   
            df = sol_new.get_value()
            if df < f:    
                print(df)
                return sol_new            
        return sol

    def choose_best(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components()
                      if len(c) <= self.k_max]
        if len(cs) < 2:
            return sol
        best, best_df = None, 0
        for c1, c2 in ((cs[x], cs[y]) for x in range(len(cs))
                                      for y in range(x+1, len(cs))):
            
            milp_model = MILPModel(sol.copy(),c1.union(c2))
            sol_new = milp_model.solve(self.time_limit,False)   
            df = sol_new.get_value()
            add = c1.union(c2)            
     
            if best is None or df < best_df:
                best, best_df = add, df
        if best is not None:
            milp_model = MILPModel(sol.copy(),best)
            sol_new = milp_model.solve(self.time_limit,False)  
        return sol_new

class MILPMergeComponentsFast(Neighborhood, ABC):
    
    def __init__(self,
                 improve: Improvement = Improvement.RANDOM,
                 k_max: int = 5, time_limit: int = 60):
        super().__init__(improve)
        self.improve = improve
        self.k_max = k_max
        self.time_limit = time_limit

    def choose_random(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components() if len(c) <= self.k_max]
        if len(cs) < 2:
            return sol
        random.shuffle(cs)                 
        milp_model = MILPModelFast(sol,cs[0].union(cs[1]))
        sol = milp_model.solve(self.time_limit,False)        
        return sol

    def choose_first(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components()
                      if len(c) <= self.k_max]
        if len(cs) < 2:
            return sol
        random.shuffle(cs)
        for c1, c2 in ((cs[x], cs[y]) for x in range(len(cs))
                                      for y in range(x+1, len(cs))):
            f = sol.get_value()
            sol_new = sol.copy()
            milp_model = MILPModelFast(sol_new,c1.union(c2))
            sol_new, A_solved = milp_model.solve(self.time_limit,False)   
            df = sol_new.get_value()
            if df < f:    
                print(df)
                return sol_new            
        return sol

    def choose_best(self, sol: Solution) -> Solution:
        cs = [c for c in sol.get_components()
                      if len(c) <= self.k_max]
        if len(cs) < 2:
            return sol
        best, best_df = None, 0
        for c1, c2 in ((cs[x], cs[y]) for x in range(len(cs))
                                      for y in range(x+1, len(cs))):
            
            milp_model = MILPModelFast(sol.copy(),c1.union(c2))
            sol_new = milp_model.solve(self.time_limit,False)   
            df = sol_new.get_value()
            add = c1.union(c2)            
     
            if best is None or df < best_df:
                best, best_df = add, df
        if best is not None:
            milp_model = MILPModelFast(sol.copy(),best)
            sol_new = milp_model.solve(self.time_limit,False)  
        return sol_new


class RandomUnionNeighborhood(Neighborhood, ABC):

    def __init__(self, improve: Improvement = Improvement.RANDOM, k_max: int = 10):
        super().__init__(improve)
        self.nbhs = [
            VertexMoveNeighborhood(improve),
            ComponentMergeNeighborhood(improve, k_max),
            VertexMoveNeighborhood(improve),
            TwoExchangeNeighborhood(improve),
            VertexMoveNeighborhood(improve),
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

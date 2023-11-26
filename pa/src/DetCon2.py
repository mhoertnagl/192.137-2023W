from Problem import Problem
from Solution import Solution


class DetCon2:

    def __init__(self, problem: Problem):
        self.__problem = problem
        self.__solution = Solution(problem)

    def construct(self):
        for (_, i, j) in self.__problem.all_edges_weighted():
            self.__solution.add_edge(i, j)
            if not self.__solution.is_feasible():
                self.__solution.remove_edge(i, j)
        return self.__solution

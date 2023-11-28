from rancon import RanCon
from solution import Solution
from localsearch import LocalSearch


class Grasper:

    def __init__(self,
                 ls: LocalSearch,
                 rc: RanCon,
                 num_iterations: int):
        self.ls = ls
        self.rc = rc
        self.num_iterations = num_iterations

    def run(self) -> Solution:
        sol = self.rc.construct()
        sol = self.ls.run(sol)
        for _ in range(self.num_iterations):
            new_sol = self.rc.construct()
            new_sol = self.ls.run(new_sol)
            if sol is None or new_sol.get_value() <= sol.get_value():
                sol = new_sol
        return sol
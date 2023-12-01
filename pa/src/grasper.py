from rancon import RanCon
from solution import Solution
from localsearch import LocalSearch
from termination import Termination


class Grasper:

    def __init__(self, rc: RanCon, ls: LocalSearch, ter: Termination):
        self.rc = rc
        self.ls = ls
        self.ter = ter

    def run(self) -> Solution:
        self.ter.init()
        sol = self.rc.construct()
        sol = self.ls.run(sol)
        while True:
            new_sol = self.rc.construct()
            new_sol = self.ls.run(new_sol)
            if self.ter.done(sol, new_sol):
                break
            if new_sol.get_value() <= sol.get_value():
                sol = new_sol.copy()
        return sol

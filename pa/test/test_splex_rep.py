from unittest import TestCase

import data
from splex.ga.population import Population
from splex.ga.rep import BestReplacer


class TestReplacer(TestCase):

    prb = data.problem_4z_s2()
    s01 = data.solution_4z_s2_01()
    s02 = data.solution_4z_s2_02()
    s03 = data.solution_4z_s2_03()
    s04 = data.solution_4z_s2_04()
    s05 = data.solution_4z_s2_05()
    s06 = data.solution_4z_s2_06()

    def test_best(self):
        par = Population([self.s02, self.s04, self.s06])
        kid = Population([self.s01, self.s03, self.s05])
        rep = BestReplacer()
        act = rep.replace(self.prb, par, kid, 3)
        exp = [self.s05, self.s03, self.s06]
        self.assertListEqual(exp, act.list())


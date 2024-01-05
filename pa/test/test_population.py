from unittest import TestCase

import data
from splex.ga.population import Population


class TestPopulation(TestCase):

    prb = data.problem_4z_s2()
    s01 = data.solution_4z_s2_01()
    s02 = data.solution_4z_s2_02()
    s03 = data.solution_4z_s2_03()
    s04 = data.solution_4z_s2_04()
    s05 = data.solution_4z_s2_05()
    s06 = data.solution_4z_s2_06()

    def test_append(self):
        pop = Population()
        self.assertListEqual([], pop.list())
        pop.append(self.s06)
        self.assertListEqual([self.s06], pop.list())
        pop.append(self.s03)
        self.assertListEqual([self.s03, self.s06], pop.list())
        pop.append(self.s04)
        self.assertListEqual([self.s03, self.s06, self.s04], pop.list())

    def test_extend(self):
        pop = Population([self.s02, self.s04, self.s06])
        self.assertListEqual([self.s06, self.s02, self.s04], pop.list())
        pop.extend([self.s01, self.s03, self.s05])
        self.assertListEqual([
            self.s05, self.s03, self.s06,
            self.s01, self.s02, self.s04
        ], pop.list())

    def test_resize(self):
        pop = Population([
            self.s01, self.s02, self.s03,
            self.s06, self.s05, self.s04,
        ])
        act = pop.resize(3)
        exp = Population([self.s06, self.s05, self.s03])
        self.assertListEqual(exp.list(), act.list())

    def test_best(self):
        pop = Population([
            self.s01, self.s02, self.s03,
            self.s06, self.s04,
        ])
        self.assertEqual(self.s03, pop.best())

    def test_probabilities(self):
        s01 = data.solution_4z_s2_01()
        s02 = data.solution_4z_s2_02()
        s03 = data.solution_4z_s2_03()
        s04 = data.solution_4z_s2_04()
        s05 = data.solution_4z_s2_05()
        s06 = data.solution_4z_s2_06()
        v01 = s01.value()
        v02 = s02.value()
        v03 = s03.value()
        v04 = s04.value()
        v05 = s05.value()
        v06 = s06.value()
        tot = v01 + v02 + v03 + v04 + v05 + v06
        pop = Population([s01, s02, s03, s04, s05, s06])
        exp = [v05/tot, v03/tot, v06/tot, v01/tot, v02/tot, v04/tot]
        act = pop.probabilities()
        self.assertAlmostEqual(exp[0], act[0])
        self.assertAlmostEqual(exp[1], act[1])
        self.assertAlmostEqual(exp[2], act[2])
        self.assertAlmostEqual(exp[3], act[3])
        self.assertAlmostEqual(exp[4], act[4])
        self.assertAlmostEqual(exp[5], act[5])
        self.assertAlmostEqual(1.0, sum(act))

from unittest import TestCase

import data
from splex.ga.population import Population
from splex.ga.sel import RankSelection, TournamentSelection


class TestSelection(TestCase):
    def test_rank_select(self):
        prb = data.problem_4z_s2()
        s01 = data.solution_4z_s2_01()
        s02 = data.solution_4z_s2_02()
        s03 = data.solution_4z_s2_03()
        s04 = data.solution_4z_s2_04()
        s05 = data.solution_4z_s2_05()
        s06 = data.solution_4z_s2_06()
        pop = Population([s01, s02, s03, s04, s05, s06])
        sel = RankSelection(6)
        exp = [s05, s03, s06, s01, s02, s04]
        act = sel.select(prb, pop)
        self.assertListEqual(exp, act.list())

    def test_tournament_select_01(self):
        prb = data.problem_4z_s2()
        s03 = data.solution_4z_s2_03()
        s05 = data.solution_4z_s2_05()
        sel = TournamentSelection(1, 2)
        act = sel.select(prb, Population([s03, s05]))
        self.assertListEqual([s05], act.list())

    def test_tournament_select_02(self):
        prb = data.problem_4z_s2()
        s01 = data.solution_4z_s2_01()
        s02 = data.solution_4z_s2_02()
        s03 = data.solution_4z_s2_03()
        s04 = data.solution_4z_s2_04()
        sel = TournamentSelection(1, 4)
        act = sel.select(prb, Population([s03, s04, s01, s02]))
        self.assertListEqual([s03], act.list())

from unittest import TestCase

from splex import Problem, Solution
from splex.ga.comb import select_components, pick_components


class Test(TestCase):

    def test_select_components(self):
        act_res, act_exc = select_components([
            frozenset([1, 2, 3]),
            frozenset([3, 4, 5]),
            frozenset([4, 5]),
            frozenset([6, 7, 8]),
            frozenset([7, 8]),
            frozenset([2, 3, 9]),
        ])
        exp_res = {
            frozenset([1, 2, 3]),
            frozenset([4, 5]),
            frozenset([6, 7, 8])
        }
        exp_exc = {9}
        self.assertSetEqual(exp_res, act_res)
        self.assertSetEqual(exp_exc, act_exc)

    def test_pick_components(self):
        act_rs1, act_rs2, act_ex = pick_components([
            frozenset([1, 2, 3]),
            frozenset([4, 5]),
            frozenset([7, 8]),
        ], [
            frozenset([3, 4, 5]),
            frozenset([6, 7, 8]),
            frozenset([2, 3, 9]),
            frozenset([1, 10]),
        ])
        exp_rs1 = {
            frozenset([1, 2, 3]),
            frozenset([4, 5]),
        }
        exp_rs2 = {
            frozenset([6, 7, 8])
        }
        exp_ex = {9, 10}
        self.assertSetEqual(exp_rs1, act_rs1)
        self.assertSetEqual(exp_rs2, act_rs2)
        self.assertSetEqual(exp_ex, act_ex)

    def test_merge_parents(self):
        pass


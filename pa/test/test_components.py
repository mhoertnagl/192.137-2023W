from unittest import TestCase

from splex.ga.comb import select_components


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

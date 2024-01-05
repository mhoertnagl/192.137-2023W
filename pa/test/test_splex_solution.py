from unittest import TestCase

import data


class TestSolution(TestCase):

    def test_delta_empty_1_2(self):
        # Solution without any edges.
        sol = data.solution_4z_s2_01()
        self.assertEqual(10, sol.value())
        # Delta should be -2 if we add 1--2.
        self.assertEqual(-2, sol.delta([(1, 2)], []))

    def test_delta_empty_1_3(self):
        # Solution without any edges.
        sol = data.solution_4z_s2_01()
        self.assertEqual(10, sol.value())
        # Delta should be 1 if we add 1--3.
        self.assertEqual(1, sol.delta([(1, 3)], []))

    def test_delta_empty_1_4(self):
        # Solution without any edges.
        sol = data.solution_4z_s2_01()
        self.assertEqual(10, sol.value())
        # Delta should be 4 if we add 1--4.
        self.assertEqual(4, sol.delta([(1, 4)], []))

    def test_delta_empty_2_3(self):
        # Solution without any edges.
        sol = data.solution_4z_s2_01()
        self.assertEqual(10, sol.value())
        # Delta should be -3 if we add 2--3.
        self.assertEqual(-3, sol.delta([(2, 3)], []))

    def test_delta_empty_2_4(self):
        # Solution without any edges.
        sol = data.solution_4z_s2_01()
        self.assertEqual(10, sol.value())
        # Delta should be 1 if we add 2--4.
        self.assertEqual(1, sol.delta([(2, 4)], []))

    def test_delta_empty_3_4(self):
        # Solution without any edges.
        sol = data.solution_4z_s2_01()
        self.assertEqual(10, sol.value())
        # Delta should be -5 if we add 3--4.
        self.assertEqual(-5, sol.delta([(3, 4)], []))

    def test_delta_remove_from_empty_1_2(self):
        # Solution without any edges.
        sol = data.solution_4z_s2_01()
        self.assertEqual(10, sol.value())
        # Delta should be 0 if we remove 1--2 which is already removed.
        self.assertEqual(0, sol.delta([], [(1, 2)]))

    #################################################################

    def test_delta_full_1_2(self):
        # Fully connected solution.
        sol = data.solution_4z_s2_06()
        self.assertEqual(6, sol.value())
        # Delta should be -2 if we add 1--2.
        self.assertEqual(-2, sol.delta([], [(1, 2)]))

    def test_delta_full_1_3(self):
        # Fully connected solution.
        sol = data.solution_4z_s2_06()
        self.assertEqual(6, sol.value())
        # Delta should be 1 if we add 1--3.
        self.assertEqual(1, sol.delta([], [(1, 3)]))

    def test_delta_full_1_4(self):
        # Fully connected solution.
        sol = data.solution_4z_s2_06()
        self.assertEqual(6, sol.value())
        # Delta should be 4 if we add 1--4.
        self.assertEqual(4, sol.delta([], [(1, 4)]))

    def test_delta_full_2_3(self):
        # Fully connected solution.
        sol = data.solution_4z_s2_06()
        self.assertEqual(6, sol.value())
        # Delta should be -3 if we add 2--3.
        self.assertEqual(-3, sol.delta([], [(2, 3)]))

    def test_delta_full_2_4(self):
        # Fully connected solution.
        sol = data.solution_4z_s2_06()
        self.assertEqual(6, sol.value())
        # Delta should be 1 if we add 2--4.
        self.assertEqual(1, sol.delta([], [(2, 4)]))

    def test_delta_full_3_4(self):
        # Fully connected solution.
        sol = data.solution_4z_s2_06()
        self.assertEqual(6, sol.value())
        # Delta should be -5 if we add 3--4.
        self.assertEqual(-5, sol.delta([], [(3, 4)]))

    def test_delta_add_to_full_1_2(self):
        # Fully connected solution.
        sol = data.solution_4z_s2_06()
        self.assertEqual(6, sol.value())
        # Delta should be 0 if we add 1--2 which is already added.
        self.assertEqual(0, sol.delta([(1, 2)], []))

    #################################################################

    def test_solution_4z_s2_01(self):
        sol = data.solution_4z_s2_01()
        self.assertTrue(sol.is_feasible())
        self.assertEqual(10, sol.value())

    def test_solution_4z_s2_02(self):
        sol = data.solution_4z_s2_02()
        self.assertTrue(sol.is_feasible())
        self.assertEqual(12, sol.value())

    def test_solution_4z_s2_03(self):
        sol = data.solution_4z_s2_03()
        self.assertTrue(sol.is_feasible())
        self.assertEqual(5, sol.value())

    def test_solution_4z_s2_04(self):
        sol = data.solution_4z_s2_04()
        self.assertTrue(sol.is_feasible())
        self.assertEqual(13, sol.value())

    def test_solution_4z_s2_05(self):
        sol = data.solution_4z_s2_05()
        self.assertTrue(sol.is_feasible())
        self.assertEqual(2, sol.value())

    def test_solution_4z_s2_06(self):
        sol = data.solution_4z_s2_06()
        self.assertTrue(sol.is_feasible())
        self.assertEqual(6, sol.value())

    def test_value(self):
        pass

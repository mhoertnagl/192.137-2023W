from unittest import TestCase

from splex import Problem


def test_problem():
    return Problem("test", 1, 5, [
        (1, 2, 1, 99),
        (1, 3, 0, 66),
        (1, 4, 0, 65),
        (1, 5, 0, 64),
        (2, 3, 0, 98),
        (2, 4, 0, 63),
        (2, 5, 0, 62),
        (3, 4, 1, 97),
        (3, 5, 0, 61),
        (4, 5, 0, 96)
    ])


class TestProblem(TestCase):
    def test_connected(self):
        problem = test_problem()
        self.assertTrue(problem.connected(1, 2))
        self.assertTrue(problem.connected(2, 1))
        self.assertFalse(problem.connected(2, 3))
        self.assertFalse(problem.connected(3, 2))
        self.assertTrue(problem.connected(3, 4))
        self.assertTrue(problem.connected(4, 3))
        self.assertFalse(problem.connected(4, 5))
        self.assertFalse(problem.connected(5, 4))
        self.assertFalse(problem.connected(3, 5))
        self.assertFalse(problem.connected(5, 3))

    def test_weight(self):
        problem = test_problem()
        self.assertEqual(problem.weight(1, 2), -99)
        self.assertEqual(problem.weight(2, 1), -99)
        self.assertEqual(problem.weight(2, 3), 98)
        self.assertEqual(problem.weight(3, 2), 98)
        self.assertEqual(problem.weight(3, 4), -97)
        self.assertEqual(problem.weight(4, 3), -97)
        self.assertEqual(problem.weight(4, 5), 96)
        self.assertEqual(problem.weight(5, 4), 96)
        self.assertEqual(problem.weight(3, 5), 61)
        self.assertEqual(problem.weight(5, 3), 61)

    def test_initial_edges(self):
        problem = test_problem()
        self.assertEqual(problem.initial_edges(), [
            (-99, 1, 2),
            (-97, 3, 4)
        ])

    def test_all_edges(self):
        problem = test_problem()
        self.assertEqual(problem.all_edges(), [
            (-99, 1, 2),
            (-97, 3, 4),
            (61, 3, 5),
            (62, 2, 5),
            (63, 2, 4),
            (64, 1, 5),
            (65, 1, 4),
            (66, 1, 3),
            (96, 4, 5),
            (98, 2, 3)
        ])

    def test_non_edges(self):
        problem = test_problem()
        self.assertEqual(problem.non_edges(), [
            (61, 3, 5),
            (62, 2, 5),
            (63, 2, 4),
            (64, 1, 5),
            (65, 1, 4),
            (66, 1, 3),
            (96, 4, 5),
            (98, 2, 3)
        ])


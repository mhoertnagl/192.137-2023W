from unittest import TestCase

from splex import Problem


class TestProblem(TestCase):
    def test_has_edge(self):
        problem = _test_problem()
        problem.has_edge(1, 2)
        problem.has_edge(2, 1)
        problem.has_edge(2, 3)
        problem.has_edge(3, 2)
        problem.has_edge(3, 4)
        problem.has_edge(4, 3)
        problem.has_edge(4, 5)
        problem.has_edge(5, 4)
        problem.has_edge(3, 5)
        problem.has_edge(5, 3)

    def test_weight(self):
        problem = _test_problem()
        problem.weight(1, 2)
        problem.weight(2, 1)
        problem.weight(2, 3)
        problem.weight(3, 2)
        problem.weight(3, 4)
        problem.weight(4, 3)
        problem.weight(4, 5)
        problem.weight(5, 4)
        problem.weight(3, 5)
        problem.weight(5, 3)

    def test_initial_edges(self):
        self.fail()

    def test_all_edges(self):
        self.fail()

    def test_non_edges(self):
        self.fail()


def _test_problem():
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
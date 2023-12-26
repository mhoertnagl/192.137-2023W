from unittest import TestCase

from benchy import Harness


class TestHarness(TestCase):
    def test_iter1(self):
        harness = Harness("test", None)
        harness.add_parameter("alpha", [False, True])
        harness.add_parameter("beta", [False, True])
        harness.add_parameter("gamma", [False, True])
        # result = [params for params in harness]
        result = list(harness)
        self.assertListEqual(result, [
            {'alpha': False, 'beta': False, 'gamma': False},
            {'alpha': False, 'beta': False, 'gamma': True},
            {'alpha': False, 'beta': True,  'gamma': False},
            {'alpha': False, 'beta': True,  'gamma': True},
            {'alpha': True,  'beta': False, 'gamma': False},
            {'alpha': True,  'beta': False, 'gamma': True},
            {'alpha': True,  'beta': True,  'gamma': False},
            {'alpha': True,  'beta': True,  'gamma': True}
        ])

    def test_iter(self):
        harness = Harness("test", None)
        harness.add_parameter("alpha", list(range(4)))
        harness.add_parameter("beta", ["a", "b", "c"])
        harness.add_parameter("gamma", [0.1, 0.2, 0.3, 0.4])
        # result = [params for params in harness]
        result = list(harness)
        self.assertListEqual(result, [
            {'alpha': 0, 'beta': 'a', 'gamma': 0.1},
            {'alpha': 0, 'beta': 'a', 'gamma': 0.2},
            {'alpha': 0, 'beta': 'a', 'gamma': 0.3},
            {'alpha': 0, 'beta': 'a', 'gamma': 0.4},
            {'alpha': 0, 'beta': 'b', 'gamma': 0.1},
            {'alpha': 0, 'beta': 'b', 'gamma': 0.2},
            {'alpha': 0, 'beta': 'b', 'gamma': 0.3},
            {'alpha': 0, 'beta': 'b', 'gamma': 0.4},
            {'alpha': 0, 'beta': 'c', 'gamma': 0.1},
            {'alpha': 0, 'beta': 'c', 'gamma': 0.2},
            {'alpha': 0, 'beta': 'c', 'gamma': 0.3},
            {'alpha': 0, 'beta': 'c', 'gamma': 0.4},
            {'alpha': 1, 'beta': 'a', 'gamma': 0.1},
            {'alpha': 1, 'beta': 'a', 'gamma': 0.2},
            {'alpha': 1, 'beta': 'a', 'gamma': 0.3},
            {'alpha': 1, 'beta': 'a', 'gamma': 0.4},
            {'alpha': 1, 'beta': 'b', 'gamma': 0.1},
            {'alpha': 1, 'beta': 'b', 'gamma': 0.2},
            {'alpha': 1, 'beta': 'b', 'gamma': 0.3},
            {'alpha': 1, 'beta': 'b', 'gamma': 0.4},
            {'alpha': 1, 'beta': 'c', 'gamma': 0.1},
            {'alpha': 1, 'beta': 'c', 'gamma': 0.2},
            {'alpha': 1, 'beta': 'c', 'gamma': 0.3},
            {'alpha': 1, 'beta': 'c', 'gamma': 0.4},
            {'alpha': 2, 'beta': 'a', 'gamma': 0.1},
            {'alpha': 2, 'beta': 'a', 'gamma': 0.2},
            {'alpha': 2, 'beta': 'a', 'gamma': 0.3},
            {'alpha': 2, 'beta': 'a', 'gamma': 0.4},
            {'alpha': 2, 'beta': 'b', 'gamma': 0.1},
            {'alpha': 2, 'beta': 'b', 'gamma': 0.2},
            {'alpha': 2, 'beta': 'b', 'gamma': 0.3},
            {'alpha': 2, 'beta': 'b', 'gamma': 0.4},
            {'alpha': 2, 'beta': 'c', 'gamma': 0.1},
            {'alpha': 2, 'beta': 'c', 'gamma': 0.2},
            {'alpha': 2, 'beta': 'c', 'gamma': 0.3},
            {'alpha': 2, 'beta': 'c', 'gamma': 0.4},
            {'alpha': 3, 'beta': 'a', 'gamma': 0.1},
            {'alpha': 3, 'beta': 'a', 'gamma': 0.2},
            {'alpha': 3, 'beta': 'a', 'gamma': 0.3},
            {'alpha': 3, 'beta': 'a', 'gamma': 0.4},
            {'alpha': 3, 'beta': 'b', 'gamma': 0.1},
            {'alpha': 3, 'beta': 'b', 'gamma': 0.2},
            {'alpha': 3, 'beta': 'b', 'gamma': 0.3},
            {'alpha': 3, 'beta': 'b', 'gamma': 0.4},
            {'alpha': 3, 'beta': 'c', 'gamma': 0.1},
            {'alpha': 3, 'beta': 'c', 'gamma': 0.2},
            {'alpha': 3, 'beta': 'c', 'gamma': 0.3},
            {'alpha': 3, 'beta': 'c', 'gamma': 0.4}
        ])

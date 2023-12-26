from unittest import TestCase

from splex.graph import Graph, find_component


class TestGraph(TestCase):

    def test_connected(self):
        g = Graph(2)
        self.assertFalse(g.connected(1, 1))
        self.assertFalse(g.connected(1, 2))
        self.assertFalse(g.connected(2, 1))
        g.add_edge(1, 2)
        self.assertFalse(g.connected(1, 1))
        self.assertTrue(g.connected(1, 2))
        self.assertTrue(g.connected(2, 1))
        g.remove_edge(1, 2)
        self.assertFalse(g.connected(1, 1))
        self.assertFalse(g.connected(1, 2))
        self.assertFalse(g.connected(2, 1))

    def test_add_edge(self):
        self.fail()

    def test_remove_edge(self):
        self.fail()

    def test_degree(self):
        g = Graph(3)
        self.assertEqual(g.degree(1), 0)
        self.assertEqual(g.degree(2), 0)
        self.assertEqual(g.degree(3), 0)
        g.add_edge(1, 2)
        self.assertEqual(g.degree(1), 1)
        self.assertEqual(g.degree(2), 1)
        self.assertEqual(g.degree(3), 0)
        g.add_edge(1, 3)
        self.assertEqual(g.degree(1), 2)
        self.assertEqual(g.degree(2), 1)
        self.assertEqual(g.degree(3), 1)
        g.add_edge(2, 3)
        self.assertEqual(g.degree(1), 2)
        self.assertEqual(g.degree(2), 2)
        self.assertEqual(g.degree(3), 2)
        g.remove_edge(1, 3)
        self.assertEqual(g.degree(1), 1)
        self.assertEqual(g.degree(2), 2)
        self.assertEqual(g.degree(3), 1)
        g.remove_edge(2, 3)
        self.assertEqual(g.degree(1), 1)
        self.assertEqual(g.degree(2), 1)
        self.assertEqual(g.degree(3), 0)
        g.remove_edge(1, 2)
        self.assertEqual(g.degree(1), 0)
        self.assertEqual(g.degree(2), 0)
        self.assertEqual(g.degree(3), 0)

    def test_neighbors(self):
        g = Graph(4)
        self.assertEqual(set(), g.neighbors(1))
        self.assertEqual(set(), g.neighbors(2))
        self.assertEqual(set(), g.neighbors(3))
        self.assertEqual(set(), g.neighbors(4))
        g.add_edge(1, 2)
        self.assertEqual({2}, g.neighbors(1))
        self.assertEqual({1}, g.neighbors(2))
        self.assertEqual(set(), g.neighbors(3))
        self.assertEqual(set(), g.neighbors(4))
        g.add_edge(1, 3)
        self.assertEqual({2, 3}, g.neighbors(1))
        self.assertEqual({1}, g.neighbors(2))
        self.assertEqual({1}, g.neighbors(3))
        self.assertEqual(set(), g.neighbors(4))
        g.add_edge(2, 4)
        self.assertEqual({2, 3}, g.neighbors(1))
        self.assertEqual({1, 4}, g.neighbors(2))
        self.assertEqual({1}, g.neighbors(3))
        self.assertEqual({2}, g.neighbors(4))
        g.add_edge(3, 4)
        self.assertEqual({2, 3}, g.neighbors(1))
        self.assertEqual({1, 4}, g.neighbors(2))
        self.assertEqual({1, 4}, g.neighbors(3))
        self.assertEqual({2, 3}, g.neighbors(4))
        g.remove_edge(4, 2)
        self.assertEqual({2, 3}, g.neighbors(1))
        self.assertEqual({1}, g.neighbors(2))
        self.assertEqual({1, 4}, g.neighbors(3))
        self.assertEqual({3}, g.neighbors(4))
        g.remove_edge(1, 2)
        self.assertEqual({3}, g.neighbors(1))
        self.assertEqual(set(), g.neighbors(2))
        self.assertEqual({1, 4}, g.neighbors(3))
        self.assertEqual({3}, g.neighbors(4))
        g.remove_edge(3, 1)
        self.assertEqual(set(), g.neighbors(1))
        self.assertEqual(set(), g.neighbors(2))
        self.assertEqual({4}, g.neighbors(3))
        self.assertEqual({3}, g.neighbors(4))
        g.remove_edge(3, 4)
        self.assertEqual(set(), g.neighbors(1))
        self.assertEqual(set(), g.neighbors(2))
        self.assertEqual(set(), g.neighbors(3))
        self.assertEqual(set(), g.neighbors(4))

    def test_component(self):
        g = Graph(4)
        self.assertEqual({1}, g.component(1))
        self.assertEqual({2}, g.component(2))
        self.assertEqual({3}, g.component(3))
        self.assertEqual({4}, g.component(4))
        g.add_edge(1, 3)
        self.assertEqual({1, 3}, g.component(1))
        self.assertEqual({2}, g.component(2))
        self.assertEqual({1, 3}, g.component(3))
        self.assertEqual({4}, g.component(4))
        g.add_edge(1, 2)
        self.assertEqual({1, 2, 3}, g.component(1))
        self.assertEqual({1, 2, 3}, g.component(2))
        self.assertEqual({1, 2, 3}, g.component(3))
        self.assertEqual({4}, g.component(4))
        g.add_edge(2, 3)
        self.assertEqual({1, 2, 3}, g.component(1))
        self.assertEqual({1, 2, 3}, g.component(2))
        self.assertEqual({1, 2, 3}, g.component(3))
        self.assertEqual({4}, g.component(4))
        g.add_edge(3, 4)
        self.assertEqual({1, 2, 3, 4}, g.component(1))
        self.assertEqual({1, 2, 3, 4}, g.component(2))
        self.assertEqual({1, 2, 3, 4}, g.component(3))
        self.assertEqual({1, 2, 3, 4}, g.component(4))
        g.add_edge(2, 4)
        self.assertEqual({1, 2, 3, 4}, g.component(1))
        self.assertEqual({1, 2, 3, 4}, g.component(2))
        self.assertEqual({1, 2, 3, 4}, g.component(3))
        self.assertEqual({1, 2, 3, 4}, g.component(4))
        g.add_edge(1, 4)
        self.assertEqual({1, 2, 3, 4}, g.component(1))
        self.assertEqual({1, 2, 3, 4}, g.component(2))
        self.assertEqual({1, 2, 3, 4}, g.component(3))
        self.assertEqual({1, 2, 3, 4}, g.component(4))
        g.remove_edge(1, 2)
        self.assertEqual({1, 2, 3, 4}, g.component(1))
        self.assertEqual({1, 2, 3, 4}, g.component(2))
        self.assertEqual({1, 2, 3, 4}, g.component(3))
        self.assertEqual({1, 2, 3, 4}, g.component(4))
        g.remove_edge(1, 3)
        self.assertEqual({1, 2, 3, 4}, g.component(1))
        self.assertEqual({1, 2, 3, 4}, g.component(2))
        self.assertEqual({1, 2, 3, 4}, g.component(3))
        self.assertEqual({1, 2, 3, 4}, g.component(4))
        g.remove_edge(4, 2)
        self.assertEqual({1, 2, 3, 4}, g.component(1))
        self.assertEqual({1, 2, 3, 4}, g.component(2))
        self.assertEqual({1, 2, 3, 4}, g.component(3))
        self.assertEqual({1, 2, 3, 4}, g.component(4))
        g.remove_edge(4, 3)
        self.assertEqual({1, 4}, g.component(1))
        self.assertEqual({2, 3}, g.component(2))
        self.assertEqual({2, 3}, g.component(3))
        self.assertEqual({1, 4}, g.component(4))
        g.remove_edge(4, 1)
        self.assertEqual({1}, g.component(1))
        self.assertEqual({2, 3}, g.component(2))
        self.assertEqual({2, 3}, g.component(3))
        self.assertEqual({4}, g.component(4))
        g.remove_edge(3, 2)
        self.assertEqual({1}, g.component(1))
        self.assertEqual({2}, g.component(2))
        self.assertEqual({3}, g.component(3))
        self.assertEqual({4}, g.component(4))

    def test_components(self):
        g = Graph(4)
        self.assertEqual([{1}, {2}, {3}, {4}], g.components())
        g.add_edge(1, 3)
        self.assertEqual([{1, 3}, {2}, {4}], g.components())
        g.add_edge(1, 2)
        self.assertEqual([{1, 2, 3}, {4}], g.components())
        g.add_edge(2, 3)
        self.assertEqual([{1, 2, 3}, {4}], g.components())
        g.add_edge(3, 4)
        self.assertEqual([{1, 2, 3, 4}], g.components())
        g.add_edge(2, 4)
        self.assertEqual([{1, 2, 3, 4}], g.components())
        g.add_edge(1, 4)
        self.assertEqual([{1, 2, 3, 4}], g.components())
        g.remove_edge(1, 2)
        self.assertEqual([{1, 2, 3, 4}], g.components())
        g.remove_edge(1, 3)
        self.assertEqual([{1, 2, 3, 4}], g.components())
        g.remove_edge(4, 2)
        self.assertEqual([{1, 2, 3, 4}], g.components())
        g.remove_edge(4, 3)
        self.assertEqual([{1, 4}, {2, 3}], g.components())
        g.remove_edge(4, 1)
        self.assertEqual([{1}, {2, 3}, {4}], g.components())
        g.remove_edge(3, 2)
        self.assertEqual([{1}, {2}, {3}, {4}], g.components())

    def test_find_component(self):
        self.assertEqual(find_component({
            1: {2},
            2: {1},
            3: {4},
            4: {3}
        }, 1), {1, 2})
        self.assertEqual(find_component({
            1: {2},
            2: {1},
            3: {4},
            4: {3}
        }, 4), {3, 4})
        self.assertEqual(find_component({
            1: {2, 3},
            2: {1, 4},
            3: {2, 4},
            4: {2, 3},
            5: set()
        }, 1), {1, 2, 3, 4})
        self.assertEqual(find_component({
            1: {2, 3},
            2: {1, 4},
            3: {2, 4},
            4: {2, 3},
            5: set()
        }, 4), {1, 2, 3, 4})
        self.assertEqual(find_component({
            1: {2, 3},
            2: {1, 4},
            3: {2, 4},
            4: {2, 3},
            5: set()
        }, 5), {5})

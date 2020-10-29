#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 2, Problem 2: Recomputing a Minimum Spanning Tree

Team Number:
Student Names:
'''

'''
Copyright: justin.pearson@it.uu.se and his teaching assistants, 2020.

This file is part of course 1DL231 at Uppsala University, Sweden.

Permission is hereby granted only to the registered students of that
course to use this file, for a homework assignment.

The copyright notice and permission notice above shall be included in
all copies and extensions of this file, and those are not allowed to
appear publicly on the internet, both during a course instance and
forever after.
'''
from src.recompute_mst_data import data  # noqa
from typing import Tuple  # noqa
from src.graph import Graph  # noqa
import unittest  # noqa


# If your solution needs a queue (like the BFS algorithm),
# then you can use this one:
from collections import deque  # noqa

# If you need to log information during tests, execution, or both,
# then you can use this library:
# Basic example:
#   logger = logging.getLogger("put name here")
#   a = 5
#   logger.debug(f"a = {a}")
import logging  # noqa

__all__ = ['update_MST_1', 'update_MST_2', 'update_MST_3', 'update_MST_4']


def update_MST_1(G: Graph, T: Graph, e: Tuple[str, str], weight: int):
    """
    Sig:  Graph G(V, E), Graph T(V, E), edge e, int ->
    Pre:
    Post:
    Ex:   TestCase 1 below
    """
    (u, v) = e
    assert(e in G and e not in T and weight > G.weight(u, v))


def update_MST_2(G: Graph, T: Graph, e: Tuple[str, str], weight: int):
    """
    Sig:  Graph G(V, E), Graph T(V, E), edge e, int ->
    Pre:
    Post:
    Ex:   TestCase 2 below
    """
    (u, v) = e
    assert(e in G and e not in T and weight < G.weight(u, v))


def update_MST_3(G: Graph, T: Graph, e: Tuple[str, str], weight: int):
    """
    Sig:  Graph G(V, E), Graph T(V, E), edge e, int ->
    Pre:
    Post:
    Ex:   TestCase 3 below
    """
    (u, v) = e
    assert(e in G and e in T and weight < G.weight(u, v))


def update_MST_4(G: Graph, T: Graph, e: Tuple[str, str], weight: int):
    """
    Sig:  Graph G(V, E), Graph T(V, E), edge e, int ->
    Pre:
    Post:
    Ex:   TestCase 4 below
    """
    (u, v) = e
    assert(e in G and e in T and weight > G.weight(u, v))


class RecomputeMstTest(unittest.TestCase):
    """
    Test Suite for minimum spanning tree problem

    Any method named "test_something" will be run when this file is
    executed. You may add your own test cases if you wish.
    (You may delete this class from your submitted solution.)
    """
    logger = logging.getLogger('RecomputeMstTest')

    def assertUndirectedEdgesEqual(self, actual, expected):
        self.assertListEqual(
            sorted(((min(u, v), max(u, v)) for u, v in actual)),
            sorted(((min(u, v), max(u, v)) for u, v in expected))
        )

    def assertGraphIsConnected(self, graph):
        if len(graph.nodes) == 0:
            return
        visited = set()
        s = graph.nodes[0]
        queue = deque([s])
        while len(queue) > 0:
            u = queue.popleft()
            visited.add(u)
            for v in graph.neighbors(u):
                if v not in visited:
                    queue.append(v)
        for u in graph.nodes:
            self.assertIn(u, visited)

    def assertEdgesInGraph(self, edges, graph):
        for edge in edges:
            self.assertIn(edge, graph)

    def test_mst1(self):
        # TestCase 1: e in graph.edges and e not in tree.edges and
        #             weight > graph.weight(u, v)
        i = 0
        for instance in data:
            graph = instance['graph'].copy()
            tree = instance['mst'].copy()
            u, v = instance['solutions'][i]['edge']
            weight = instance['solutions'][i]['weight']
            expected = instance['solutions'][i]['expected']
            update_MST_1(graph, tree, (u, v), weight)
            self.assertUndirectedEdgesEqual(
                tree.edges,
                expected
            )

    def test_mst2(self):
        # TestCase 2: e in graph.edges and not e in tree.edges and
        #             weight < graph.weight(u, v)
        i = 1
        for instance in data:
            graph = instance['graph'].copy()
            tree = instance['mst'].copy()
            u, v = instance['solutions'][i]['edge']
            weight = instance['solutions'][i]['weight']
            expected = instance['solutions'][i]['expected']
            update_MST_2(graph, tree, (u, v), weight)
            self.assertUndirectedEdgesEqual(
                tree.edges,
                expected
            )

    def test_mst3(self):
        # TestCase 3: e in graph.edges and e in tree and
        #             weight < graph.weight(u, v)
        i = 2
        for instance in data:
            graph = instance['graph'].copy()
            tree = instance['mst'].copy()
            u, v = instance['solutions'][i]['edge']
            weight = instance['solutions'][i]['weight']
            expected = instance['solutions'][i]['expected']
            update_MST_3(graph, tree, (u, v), weight)
            self.assertUndirectedEdgesEqual(
                tree.edges,
                expected
            )

    def test_mst4(self):
        # TestCase 4: e in graph.edges and e in tree and
        #             weight > graph.weight(u, v)
        i = 3
        for instance in data:
            graph = instance['graph'].copy()
            tree = instance['mst'].copy()
            u, v = instance['solutions'][i]['edge']
            weight = instance['solutions'][i]['weight']
            expected = instance['solutions'][i]['expected']
            expected_G = graph.copy()
            expected_G.set_weight(u, v, weight)
            update_MST_4(graph, tree, (u, v), weight)
            self.assertEdgesInGraph(tree.edges, expected_G)
            self.assertGraphIsConnected(tree)
            self.assertEqual(
                sum(graph.weight(u, v) for u, v in tree.edges),
                sum(graph.weight(u, v) for u, v in expected)
            )
            for u, v in tree.edges:
                self.assertEqual(
                    tree.weight(u, v),
                    expected_G.weight(u, v)
                )


if __name__ == '__main__':
    # Set logging config to show debug messages.
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

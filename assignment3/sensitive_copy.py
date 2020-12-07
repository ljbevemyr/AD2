#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 3, Problem 1: Controlling the Maximum Flow

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
from typing import *  # noqa
import unittest  # noqa
import math  # noqa
from src.sensitive_data import data  # noqa
from src.graph import Graph  # noqa
# If your solution needs a queue, then you can use this one:
from collections import deque  # noqa
# If you need to log information during tests, execution, or both,
# then you can use this library:
# Basic example:
#   logger = logging.getLogger('put name here')
#   a = 5
#   logger.debug(f"a = {a}")
import logging  # noqa

__all__ = ['sensitive']

def dfs_residual(G: Graph, R: Graph, node: str, nodes: Set[str]):
    nodes.add(node)
    for neighbor in G.neighbors(node):
        capacity = G.capacity(node, neighbor)
        flow = G.flow(node, neighbor)
        R.add_edge(neighbor, node, capacity=flow, flow=0)
        if neighbor not in nodes:
            dfs_residual(G, R, neighbor, nodes)

def dfs_find_reachable(R: Graph, node: str, reachable: Set[str]):
    reachable.add(node)
    for neighbor in R.neighbors(node):
        avalable_capacity = R.capacity(node, neighbor) - R.flow(node, neighbor)
        if (neighbor not in reachable and avalable_capacity != 0):
            dfs_find_reachable(R, neighbor, reachable)


def sensitive(G: Graph, s: str, t: str) -> Tuple[str, str]:
    """
    Sig:  Graph G(V,E), str, str -> Tuple[str, str]
    Pre:
    Post:
    Ex:   sensitive(g1, 'a', 'f') = ('b', 'd')
    """
    R = G.copy()
    nodes = set()
    dfs_residual(G, R, s, nodes)

    reachable = set()
    dfs_find_reachable(R, s, reachable)

    for (u, v) in G.edges:
         if u in reachable and v not in reachable:
             return (u, v)

class SensitiveTest(unittest.TestCase):
    """
    Test suite for the sensitive edge problem
    """
    logger = logging.getLogger('SensitiveTest')

    def test_sanity(self):
        """Sanity check"""
        g1 = Graph(is_directed=True)
        g1.add_edge('a', 'b', capacity=16, flow=12)
        g1.add_edge('a', 'c', capacity=13, flow=11)
        g1.add_edge('b', 'd', capacity=12, flow=12)
        g1.add_edge('c', 'b', capacity=4, flow=0)
        g1.add_edge('c', 'e', capacity=14, flow=11)
        g1.add_edge('d', 'c', capacity=9, flow=0)
        g1.add_edge('d', 'f', capacity=20, flow=19)
        g1.add_edge('e', 'd', capacity=7, flow=7)
        g1.add_edge('e', 'f', capacity=4, flow=4)
        self.assertIn(
            sensitive(g1, 'a', 'f'),
            [('b', 'd'), ('e', 'd'), ('e', 'f')]
        )
        g2 = Graph(is_directed=True)
        g2.add_edge('a', 'b', capacity=1, flow=1)
        g2.add_edge('a', 'c', capacity=100, flow=4)
        g2.add_edge('b', 'c', capacity=100, flow=1)
        g2.add_edge('c', 'd', capacity=5, flow=5)
        self.assertEqual(
            sensitive(g2, 'a', 'd'),
            ('c', 'd')
        )

    def test_sensitive(self):
        for instance in data:
            graph = instance['digraph'].copy()
            u, v = sensitive(graph, instance["source"], instance["sink"])
            self.assertIn(u, graph, f"Invalid edge ({u}, {v})")
            self.assertIn((u, v), graph, f"Invalid edge ({u}, {v})")
            self.assertIn(
                (u, v),
                instance["sensitive_edges"]
            )

if __name__ == "__main__":
    # Set logging config to show debug messages.
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

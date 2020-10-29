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
from src.sensitive_data import data  # noqa
from typing import Tuple  # noqa
from src.graph import Graph  # noqa
import unittest  # noqa

# If your solution needs a queue (like the BFS algorithm),
# then you can use this one:
from collections import deque  # noqa

# If you need to log information during tests, execution, or both,
# then you can use this library:
# Basic example:
#   logger = logging.getLogger('put name here')
#   a = 5
#   logger.debug(f"a = {a}")
import logging  # noqa

__all__ = ['sensitive']


def sensitive(G: Graph, s: str, t: str) -> Tuple[str, str]:
    """
    Sig:  Graph G(V,E), str, str -> Tuple[str, str]
    Pre:
    Post:
    Ex:   sensitive(g1, 'a', 'f') = ('b', 'd')
    """
    return None, None


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
        self.assertEqual(
            sensitive(g1, 'a', 'f'),
            ('b', 'd')
        )
        g2 = Graph(is_directed=True)
        g2.add_edge('a', 'b', capacity=1, flow=1)
        g2.add_edge('a', 'c', capacity=100, flow=4)
        g2.add_edge('b', 'c', capacity=100, flow=1)
        g2.add_edge('c', 'd', capacity=5, flow=5)
        self.assertIn(
            sensitive(g2, 'a', 'd'),
            set([('a', 'c'), ('c', 'd')])
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

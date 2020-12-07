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

def dfs(GRes: Graph, node: str, reachable: Set[str]):
    """
    Sig:  T: Graph, node: str, nodes: Set[str] ->
    Pre:  node must exist in T and nodes must be empty.
    Post: nodes contains all visited nodes
    Ex:   T = <V=(a,b,c,d,e), E=((a, b),(b, c),(c, d))>
          node = 'a'
          nodes = {}
          dfs(T, node, nodes)
          nodes is now {a,b,c,d}
    """
    reachable.add(node)
    for neighbour in GRes.neighbors(node):
        # Variant: len(T.neighbors(node)) - T.neighbors.index(neighbour)
        if neighbour not in reachable:
            dfs(GRes, neighbour, reachable)
            # Variant: len(T.nodes) - len(nodes)

def sensitive(G: Graph, s: str, t: str) -> Tuple[str, str]:
    """
    Sig:  Graph G(V,E), str, str -> Tuple[str, str]
    Pre:
    Post:
    Ex:   sensitive(g1, 'a', 'f') = ('b', 'd')
    """
    
    # Create residual graph
    GRes = Graph(is_directed=True)
    for (u, v) in G.edges:
        residual = G.capacity(u, v) - G.flow(u, v)

        if residual == 0: # Have used up all the capacity already
            GRes.add_edge(v, u, capacity=G.capacity(u, v))
        elif residual == G.capacity(u, v): # Have used none of the capacity yet
            GRes.add_edge(u, v, capacity=G.capacity(u, v))
        else:
            GRes.add_edge(u, v, capacity=residual)
            GRes.add_edge(v, u, capacity=G.flow(u, v))

    # Run DFS from the source to find which are reachable in the residual graph
    reachable = set()
    dfs(GRes, s, reachable)

    # Check for edges that go from a reachable edge to a non-reachable edge
    for (u, v) in G.edges:
        if u in reachable and v not in reachable:
            return (u, v)
    
    # If for some reason no such edge would exist
    return (None, None) 
    
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

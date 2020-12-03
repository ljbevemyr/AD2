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

def dfs2(G: Graph, node: str, last: str, reachable):
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

    if node == last:
        return True

    for neighbour in G.neighbors(node):
        print(f'node: {node}')
        print(f'neigh: {neighbour}')

        # Variant: len(T.neighbors(node)) - T.neighbors.index(neighbour)
        if neighbour not in reachable:
            if dfs2(G, neighbour, last, reachable):
                return True

    return False 
                

                  

def dfs1(G: Graph, node: str, last: str, nodes: Set[str], sens):
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

    nodes.add(node)
    
    for neighbour in G.neighbors(node):
        print(f'node: {node}')
        print(f'neighbour: {neighbour}')
        # Variant: len(T.neighbors(node)) - T.neighbors.index(neighbour)

        if neighbour not in nodes:
            if (G.flow(node, neighbour) == G.capacity(node, neighbour)):
                print((node, neighbour))
                sens.add((node, neighbour))
            else:
                dfs1(G, neighbour, last, nodes, sens)
                # Variant: len(T.nodes) - len(nodes)


def sensitive(G: Graph, s: str, t: str) -> Tuple[str, str]:
    """
    Sig:  Graph G(V,E), str, str -> Tuple[str, str]
    Pre:
    Post:
    Ex:   sensitive(g1, 'a', 'f') = ('b', 'd')
    """
    nodes  = set()
    potential_sens = set()
    #reachable = set()
    dfs1(G, s, t, nodes, potential_sens)

    sens = set()
    for edge in potential_sens:
        if dfs2(G, edge[1], t, nodes):
            sens.add(edge)
    # Ta fram alla non-reachable

    # Ny dfs
    print(f'sens: {sens}')
    return sens.pop()

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
        for i, instance in enumerate(data):
            print(f'INSTANCE: {instance}')
            print(i)
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

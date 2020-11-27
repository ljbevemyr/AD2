#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 2, Problem 2: Recomputing a Minimum Spanning Tree

Team Number: 11
Student Names: Lisa Bevemyr and Maja Danielsson
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
from typing import Tuple, Set  # noqa
from src.graph import Graph  # noqa
from math import inf
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

def dfs(T: Graph, node: str, nodes: Set[str]):
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
    for neighbour in T.neighbors(node):
        # Variant: len(T.neighbors(node)) - T.neighbors.index(neighbour)
        if neighbour not in nodes:
            dfs(T, neighbour, nodes)
            # Variant: len(T.nodes) - len(nodes)

def update_MST_4(G: Graph, T: Graph, e: Tuple[str, str], weight: int):
    """
    Sig:  Graph G(V, E), Graph T(V, E), edge e, int ->
    Pre:
    Post:
    Ex:   TestCase 4 below
    """

    (u, v) = e
    assert(e in G and e in T and weight > G.weight(u, v))

    G.set_weight(u, v, weight)
    T.remove_edge(u, v)
    a_nodes = set()
    dfs(T, u, a_nodes)

    all_edges = G.edges

    min_edge = e
    for (l, m) in all_edges:
        # Variant: len(all_edges) - all_edges.index((l, m))
        if (l in a_nodes and m not in a_nodes) or (m in a_nodes and l not in a_nodes):
            (u, v) = min_edge
            if G.weight(l, m) < G.weight(u, v):
                min_edge = (l, m)

    (u, v) = min_edge
    T.add_edge(u, v, G.weight(u, v))






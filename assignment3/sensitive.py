#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 3, Problem 1: Controlling the Maximum Flow

Team Number: 11
Student Names: Lisa Bevemyr & Maja Danielsson
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
from src.sensitive_data import data  # noqa
from src.graph import Graph  # noqa
import logging  # noqa

__all__ = ['sensitive']

def dfs(GRes: Graph, node: str, reachable: Set[str]):
    """
    Sig:  GRes: Graph, node: str, reachable: Set[str] ->
    Pre:  node must exist in GRes and reachable must be empty.
    Post: reachable contains all visited nodes
    Ex:   GRes = <V=(a,b,c,d), E=((a, c),(b, a),(b, c),(c, a),(c, b),(d, c)), 
                  (c((a,c))=96,c((b,a))=1,c((b,c))=99,c((c,a))=4,c((c,b))=1,c((d,c))=5)>>
          node = 'a'
          reachable = {}
          dfs(T, node, reachable)
          reachable is now {'b', 'c', 'a'}
    """
    reachable.add(node)
    for neighbour in GRes.neighbors(node):
        # Variant: len(GRes.neighbors(node)) - GRes.neighbors.index(neighbour)
        if neighbour not in reachable:
            dfs(GRes, neighbour, reachable)
            # Variant: len(GRes.nodes) - len(reachable)

def sensitive(G: Graph, s: str, t: str) -> Tuple[str, str]:
    """
    Sig:  Graph G(V,E), str, str -> Tuple[str, str]
    Pre:
    Post:
    Ex:   sensitive(g1, 'a', 'f') = ('b', 'd')
    """
    
    GRes = Graph(is_directed=True)
    for (u, v) in G.edges:
        # Variant: len(G.edges) - G.edges.index((u, v))
        residual = G.capacity(u, v) - G.flow(u, v)

        if residual == 0:
            GRes.add_edge(v, u, capacity=G.capacity(u, v))
        elif residual == G.capacity(u, v):
            GRes.add_edge(u, v, capacity=G.capacity(u, v))
        else:
            GRes.add_edge(u, v, capacity=residual)
            GRes.add_edge(v, u, capacity=G.flow(u, v))

    reachable = set()
    dfs(GRes, s, reachable)

    for (u, v) in G.edges:
        # Variant: len(G.edges) - G.edges.index((u, v))
        if u in reachable and v not in reachable:
            return (u, v)
    
    return (None, None) 
    

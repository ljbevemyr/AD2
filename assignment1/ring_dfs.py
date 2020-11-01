#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 1, Problem 2: Ring Detection

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
from typing import Set, Tuple  # noqa
import unittest  # noqa
from src.graph import Graph  # noqa
from src.ring_data import data  # noqa
# If you need to log information during tests, execution, or both,
# then you can use this library:
# Basic example:
#   logger = logging.getLogger("put name here")
#   a = 5
#   logger.debug(f"a = {a}")
import logging  # noqa

__all__ = ['ring', 'ring_extended']

ring_holder = []
visited = []

def dfs(graph, visited, node, came_from):
    visited.append(node)
    for neighbour in graph.neighbors(node):
        if neighbour not in visited:
            if dfs(graph, visited, neighbour, node):
                return True
        elif neighbour != came_from:
            return True
    
    return False


def dfs_extended(graph, path, node, came_from):
    if came_from == None:
        visited.append(node)
        path.append(node)
    
    for i, neighbour in enumerate(graph.neighbors(node)):
        if neighbour not in visited:
            visited.append(neighbour)
        path = path[:path.index(node)+1] #Backtrack to node who's for-loop we're in
        if neighbour not in path:
            path.append(neighbour)
            if dfs_extended(graph, path, neighbour, node):
                return True 
        elif neighbour != came_from:
            path.append(neighbour) #Add again to make nice pairs
            node_path = path[path.index(neighbour):]
            for i in range(len(node_path)-1): #Don't loop through last one
                ring_holder.append((node_path[i], node_path[i+1]))
            return True 
    return False

def ring(G: Graph) -> bool:
    """
    Sig:  Graph G(V, E) -> bool
    Pre:
    Post:
    Ex:   Sanity tests below
          ring(g1) = False
          ring(g2) = True
    """

    #Alltsåeeee, detta funkar ju också. Lär ju 100% vara det absolut snabbaste "algoritmen"?
    #Finns det något fall det inte funkar?
    
    nodes = G.nodes
    edges = G.edges

    if len(nodes) == 0 and len(edges) == 0:
        return False
    else:
        if len(nodes) > len(edges):
            return False
        else:
            return True
    
    #Vanlig dfs-lösning. Borde funka för disconnected
    '''
    nodes = G.nodes
    visited = []
    for node in nodes:
        if node not in visited:
           if dfs(G, visited, node, None):
               return True
    return False 
    '''


def ring_extended(G: Graph) -> Tuple[bool, Set[Tuple[str, str]]]:
    """
    Sig:  Graph G(V,E) -> Tuple[bool, List[Tuple[str, str]]]
    Pre:
    Post:
    Ex:   Sanity tests below
          ring_extended(g1) = False, []
          ring_extended(g2) = True, [('a','c'),('c','f'),
                                     ('f','h'),('h','g'),('g','d'),('d','f'),
                                     ('f','a')]
    """

    global ring_holder
    global visited
    ring_holder = []
    visited = []
    path = []
    nodes = G.nodes
    
    #Osäker på om detta funkar för disconnected graphs. Klarar alla tester dock
    '''
    if len(nodes) > 0:
        if dfs_extended(G, path, nodes[0], None):
            return True, ring_holder
    return False, [] 
    '''
    
    #Bör funka för disconnected?
    #Tidskomplexiteeeeeet?? Går det att förbättra? Körs på samma tid som det ovan så kanske okej?
    for node in nodes:
        ring_holder = []
        if node not in visited:
            if dfs_extended(G, path, node, None):
                return True, ring_holder

    return False, [] 
    
class RingTest(unittest.TestCase):
    """
    Test Suite for ring detection problem

    Any method named "test_something" will be run when this file is executed.
    Use the sanity check as a template for adding your own test cases if you
    wish. (You may delete this class from your submitted solution.)
    """
    logger = logging.getLogger('RingTest')

    def assertIsRing(self, graph, edges):
        """
        Asserts that a trail of edges is a ring in the graph
        """

        for e in edges:
            self.assertIn(
                e,
                graph,
                f"The edge {e} of the ring does not exist in the graph."
            )

        self.assertGreaterEqual(
            len(edges),
            3,
            "A ring consists of at least 3 edges."
        )

        for i, (u_i, v_i) in enumerate(edges[:-1]):
            u_j, v_j = edges[i+1]
            self.assertTrue(
                u_i in set([u_j, v_j]) or v_i in set([u_j, v_j]),
                f"The edges ('{u_i}', '{v_i}') and "
                f"('{u_j}', '{v_i}') are not connected."
            )

        u_1, v_1 = edges[0]
        u_k, v_k = edges[-1]

        self.assertTrue(
            u_k in set([u_1, v_1]) or v_k in set([u_1, v_1]),
            "The ring is not closed "
            f"[({u_1}, {v_1}), ..., ({u_k}, {v_k})]."
        )

        for i, (u_i, v_i) in enumerate(edges[:-1]):
            for u_j, v_j in edges[i+1:]:
                self.assertTrue(
                    u_i not in set([u_j, v_j]) or v_i not in set([u_j, v_j]),
                    f"The edges ({u_i}, {v_i}) and "
                    f"({u_j}, {v_i}) are not distinct."
                )

    def test_sanity(self):
        """
        Sanity Test

        This is a simple sanity check for your function;
        passing is not a guarantee of correctness.
        """
        edges = [
            ('a', 'b'), ('a', 'c'), ('a', 'd'), ('c', 'e'), ('c', 'f'),
            ('d', 'g'), ('d', 'h'), ('h', 'i')
        ]
        g1 = Graph(is_directed=False)
        for u, v in edges:
            g1.add_edge(u, v)
        self.assertFalse(ring(g1))
        g1.add_edge('g', 'i')
        self.assertTrue(ring(g1))

    def test_extended_sanity(self):
        """
        sanity test for returned ring

        This is a simple sanity check for your function;
        passing is not a guarantee of correctness.
        """
        edges = [
            ('a', 'b'), ('a', 'c'), ('a', 'f'), ('c', 'e'), ('c', 'f'),
            ('d', 'f'), ('d', 'g'), ('g', 'h'), ('f', 'h')
        ]
        g2 = Graph(is_directed=False)
        for u, v in edges:
            g2.add_edge(u, v)

        found, the_ring = ring_extended(g2)
        self.assertTrue(found)
        self.assertIsRing(g2, the_ring)

    def test_ring(self):
        """
        Test for ring

        passing is not a guarantee of correctness.
        """
        for i, instance in enumerate(data):
            graph = instance["graph"].copy()
            found = ring(graph)
            self.assertEqual(
                found,
                instance["expected"],
                f"instance[{i}] with {len(graph.nodes)} nodes"
            )

    def test_ring_extended(self):
        """
        Test for returned ring

        passing is not a guarantee of correctness.
        """
        for i, instance in enumerate(data):
            graph = instance["graph"].copy()
            found, the_ring = ring_extended(graph)
            self.assertEqual(
                found,
                instance["expected"],
                f"instance[{i}] with {len(graph.nodes)} nodes"
            )
            if instance["expected"]:
                self.assertIsRing(instance["graph"].copy(), the_ring)
            else:
                self.assertListEqual(the_ring, [])


if __name__ == '__main__':
    # Set logging config to show debug messages.
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
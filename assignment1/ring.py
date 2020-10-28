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


def ring(G: Graph) -> bool:
    """
    Sig:  Graph G(V, E) -> bool
    Pre:
    Post:
    Ex:   Sanity tests below
          ring(g1) = False
          ring(g2) = True
    """


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

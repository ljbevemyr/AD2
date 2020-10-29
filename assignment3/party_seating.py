#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 3, Problem 2: Party Seating

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
from src.party_seating_data import data  # noqa
from typing import List, Tuple  # noqa
import unittest  # noqa

# If your solution needs a queue, then you can use this one:
from collections import deque  # noqa

# If you need to log information during tests, execution, or both,
# then you can use this library:
# Basic example:
#   logger = logging.getLogger('put name here')
#   a = 5
#   logger.debug(f"a = {a}")
import logging  # noqa

__all__ = ['party']


def party(known: List[List[int]]) -> Tuple[bool, List[int], List[int]]:
    """
    Sig:  List[List[int]] -> Tuple[bool, List[int], List[int]]
    Pre:
    Post:
    Ex:   party([[1, 2], [0], [0]]) = True, [0], [1, 2]
    """
    return False, [], []


class PartySeatingTest(unittest.TestCase):
    """
    Test suite for party seating problem
    """
    logger = logging.getLogger('PartySeatingTest')

    def known_test(self, known, A, B):
        self.assertEqual(
            len(A) + len(B),
            len(known),
            "wrong number of guests: "
            f"{len(known)} guests, "
            f"tables hold {len(A)} and {len(B)}"
        )
        for g in range(len(known)):
            self.assertTrue(
                g in A or g in B,
                f"Guest {g} not seated anywhere"
            )
        for a1, a2 in ((a1, a2) for a2 in A for a1 in A):
            self.assertNotIn(
                a2,
                known[a1],
                f"Guests {a1} and {a2} seated together, and know each other"
            )
        for b1, b2 in ((b1, b2) for b2 in B for b1 in B):
            self.assertNotIn(
                b2,
                known[b1],
                f"Guests {b1} and {b2} seated together, and know each other"
            )

    def test_sanity(self):
        """
        Sanity test

        A minimal test case.
        """
        known = [[1, 2], [0], [0]]
        _, A, B = party(known)
        self.known_test(known, A, B)

    def test_party(self):
        for instance in data:
            known = instance["known"]
            expected = instance["expected"]
            success, A, B = party(known)

            if not expected:
                self.assertFalse(success)
                continue
            self.known_test(known, A, B)


if __name__ == '__main__':
    # Set logging config to show debug messages.
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

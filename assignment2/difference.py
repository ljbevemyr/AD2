#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 2, Problem 1: Search String Replacement

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
from src.difference_data import data  # noqa
from typing import Dict, Tuple  # noqa
import math  # noqa
import unittest  # noqa
from collections import defaultdict  # noqa
from string import ascii_lowercase  # noqa

# If you need to log information during tests, execution, or both,
# then you can use this library:
# Basic example:
#   logger = logging.getLogger("put name here")
#   a = 5
#   logger.debug(f"a = {a}")
import logging  # noqa


# Solution to Task B:
def min_difference(u: str, r: str, R: Dict[str, Dict[str, int]]) -> int:
    """
    Sig:  str, str, Dict[str, Dict[str, int]] -> int
    Pre:  For all characters c in u and k in r,
          then R[c][k] exists, and R[k][c] exists.
    Post:
    Ex:   Let R be the resemblance matrix where every change and skip
          costs 1
          min_difference("dinamck", "dynamic", R) --> 3
    """
    # To get the resemblance between two letters, use code like this:
    # difference = R['a']['b']
    #print('NEW')
    #u is x-axis and r is y-axix
    DP = [ [ None for i in range(len(u)+1) ] for j in range(len(r)+1) ]

    for i in range(len(r)+1):
        #print(f'i: {i}')
        for j in range(len(u)+1):
            #print(f'j: {j}')
            if i == 0 and j == 0:
                DP[i][j] = R['-']['-']

            elif i == 0:
                DP[i][j] = R[u[j-1]]['-']

            elif j == 0:
                DP[i][j] = R['-'][r[i-1]]
            else:
                '''
                fnutt = '-'
                print(f'u: {u[j-1]}')
                print(f'r: {r[i-1]}')
                print(f'Replace: {R[u[j-1]][r[i-1]] + DP[i-1][j-1]}')
                print(f'Insert:  {R[fnutt][r[i-1]] + DP[i][j-1]}')
                print(f'Remove:  {R[u[j-1]][fnutt] + DP[i-1][j]}')
                print(DP[i-2][j-2])
                '''
                '''
                DP[i][j] = min((R[u[j-1]][r[i-1]] + DP[i-1][j-1]),    #REPLACE
                                (R['-'][r[i-1]] + DP[i-1][j]),        #INSERT (skip in r)
                                (R[u[j-1]]['-'] + DP[i][j-1]))        #REMOVE (skip in u)                         
                '''
                DP[i][j] = min((R[u[j-1]][r[i-1]] + DP[i-1][j-1]),    #REPLACE
                                (R['-'][r[i-1]] + DP[i][j-1]),        #INSERT (skip in r)
                                (R[u[j-1]]['-'] + DP[i-1][j]))        #REMOVE (skip in u)
    '''
    for row in DP:
        print(row)
    '''
    return DP[len(r)][len(u)]

# Solution to Task C:
def min_difference_align(u: str, r: str,
                         R: Dict[str, Dict[str, int]]) -> Tuple[int, str, str]:
    """
    Sig:  str, str, Dict[str, Dict[str, int]] -> Tuple[int, str, str]
    Pre:  For all characters c in u and k in r,
          then R[c][k] exists, and R[k][c] exists.
    Post:
    Ex:   Let R be the resemblance matrix where every change and skip
          costs 1
          min_difference_align("dinamck", "dynamic", R) -->
                                    3, "dinam-ck", "dynamic-"
    """

    print('NEW')
    #u is x-axis and r is y-axix
    # [Value, Direction] 1=Diagonal=Replace, 2=Up=Insert, 3=Left=Remove
    DP = [ [ [None, None] for i in range(len(u)+1) ] for j in range(len(r)+1) ]
    res_u = ""
    res_r = ""
    for i in range(len(r)+1):
        print(f'i: {i}')
        for j in range(len(u)+1):
            print(f'j: {j}')
            if i == 0 and j == 0:
                DP[i][j][0] = R['-']['-']

            elif i == 0:
                DP[i][j][0] = R[u[j-1]]['-']
                DP[i][j][1] = 3

            elif j == 0:
                DP[i][j][0] = R['-'][r[i-1]]
                DP[i][j][1] = 2
            else:
                fnutt = '-'

                '''
                --polyn-om-ial
                exp-o-ne-ntial

                '''
                replace = R[u[j-1]][r[i-1]] + DP[i-1][j-1][0]
                insert = R['-'][r[i-1]] + DP[i-1][j][0]
                remove = R[u[j-1]]['-'] + DP[i][j-1][0]

                if (i == 8 and j == 7):
                    print(f'u: {u[j-1]}')
                    print(f'r: {r[i-1]}')
                    print(f'Replace: {replace}')
                    print(f'Insert:  {insert}')
                    print(f'Remove:  {remove}')

                operations = [replace, insert, remove]
                min_cost = min(operations)
                min_operation = operations.index(min_cost)

                DP[i][j][0] = min_cost
                DP[i][j][1] = min_operation+1

    current = [len(r), len(u)]
    for k in range(len(u)+len(r)+1):
        print(f"current: {current[0]}, {current[1]}")
        if current[0] == 0 and current[1] == 0:
            break
        '''
        elif current[0] == 0:
            res_u = '-' + res_u
            res_r = r[current[0]-1] + res_r
            current[1] -= 1
        elif current[1] == 0:
            res_u = u[current[1]-1] + res_u
            res_r = '-' + res_r
            current[0] -= 1
        '''
        #Vi har antagligen blandat ihop up/down(left)
        direction = DP[current[0]][current[1]][1]
        if direction == 1: #REPLACE
            res_u = u[current[1]-1] + res_u
            res_r = r[current[0]-1] + res_r
            current[0] -= 1
            current[1] -= 1
        elif direction == 2: #INSERT
            res_u = '-' + res_u
            res_r = r[current[0]-1] + res_r
            current[0] -= 1
        elif direction == 3: #DELETE
            res_u = u[current[1]-1] + res_u
            res_r = '-' + res_r
            current[1] -= 1


    print(f'res_u: {res_u}')
    print(f'res_r: {res_r}')
    for row in DP:
        print(row)

    return (DP[len(r)][len(u)][0], res_u, res_r)

# Sample matrix provided by us:
def qwerty_distance() -> Dict[str, Dict[str, int]]:
    """
    Generates a QWERTY Manhattan distance resemblance matrix

    Costs for letter pairs are based on the Manhattan distance of the
    corresponding keys on a standard QWERTY keyboard.
    Costs for skipping a character depends on its placement on the keyboard:
    adding a character has a higher cost for keys on the outer edges,
    deleting a character has a higher cost for keys near the middle.

    Usage:
        R = qwerty_distance()
        R['a']['b']  # result: 5
    """
    R = defaultdict(dict)
    R['-']['-'] = 0
    zones = ["dfghjk", "ertyuislcvbnm", "qwazxpo"]
    keyboard = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    for row, content in enumerate(zones):
        for char in content:
            R['-'][char] = row + 1
            R[char]['-'] = 3 - row
    for a, b in ((a, b) for b in ascii_lowercase for a in ascii_lowercase):
        row_a, pos_a = next(
            (row, content.index(a))
            for row, content in enumerate(keyboard) if a in content
        )
        row_b, pos_b = next(
            (row, content.index(b))
            for row, content in enumerate(keyboard) if b in content
        )
        R[a][b] = int(
            math.fabs(row_b - row_a) + math.fabs(pos_a - pos_b)
        )
    return R


class MinDifferenceTest(unittest.TestCase):
    """
    Test Suite for search string replacement problem

    Any method named "test_something" will be run when this file is
    executed. Use the sanity check as a template for adding your own test
    cases if you wish.
    (You may delete this class from your submitted solution.)
    """
    logger = logging.getLogger('MinDifferenceTest')
    '''
    def test_diff_sanity(self):
        """
        Difference sanity test

        Given a simple resemblance matrix, test that the reported
        difference is the expected minimum. Do NOT assume we will always
        use this resemblance matrix when testing!
        """
        alphabet = ascii_lowercase + '-'
        # The simplest (reasonable) resemblance matrix:
        R = {
            a: {b: (0 if a == b else 1) for b in alphabet} for a in alphabet
        }
        # Warning: we may (read: 'will') use another matrix!
        self.assertEqual(min_difference("d", "l", R), 1)
    '''
    def test_align_sanity(self):
        """
        Simple alignment

        Passes if the returned alignment matches the expected one.
        """
        # QWERTY resemblance matrix:
        R = qwerty_distance()
        #alphabet = ascii_lowercase + '-'
        #R = {
            #a: {b: (0 if a == b else 1) for b in alphabet} for a in alphabet
        #}
        difference, u, r = min_difference_align(
            "polynomial",
            "exponential",
            R
        )
        # Warning: we may (read: 'will') use another matrix!
        self.assertEqual(difference, 15)
        # Warning: there may be other optimal matchings!
        if u != '--polyn-om-ial':
            self.logger.warning(f"'{u}' != '--polyn-om-ial'")
        if r != 'exp-o-ne-ntial':
            self.logger.warning(f"'{r}' != 'exp-o-ne-ntial'")
    '''
    def test_min_difference(self):
        R = qwerty_distance()
        for instance in data:
            difference = min_difference(
                instance["u"],
                instance["r"],
                R
            )
            print(instance["u"])
            print(instance["r"])
            self.assertEqual(instance["expected"], difference)
    '''
    '''
    def test_min_difference_align(self):
        R = qwerty_distance()
        for instance in data:
            difference, u, r = min_difference_align(
                instance["u"],
                instance["r"],
                R
            )
            self.assertEqual(instance["expected"], difference)
            self.assertEqual(len(u), len(r))
            u_diff, _, _ = min_difference_align(u, instance["u"], R)
            self.assertEqual(u_diff, 0)
            r_diff, _, _ = min_difference_align(r, instance["r"], R)
            self.assertEqual(r_diff, 0)
    '''
if __name__ == '__main__':
    # Set logging config to show debug messages.
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

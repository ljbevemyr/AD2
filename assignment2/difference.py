#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 2, Problem 1: Search String Replacement

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
    Post: None
    Ex:   Let R be the resemblance matrix where every change and skip
          costs 1
          min_difference("dinamck", "dynamic", R) --> 3
    """
    # To get the resemblance between two letters, use code like this:
    # difference = R['a']['b']
    #u is x-axis and r is y-axix
    DP = [ [ None for i in range(len(u)+1) ] for j in range(len(r)+1) ]
    # Inner loop variant: len(u)+1 - i
    # Outer loop variant: len(r)+1 - j

    for i in range(len(r)+1):
        # Variant: len(r)+1 - i
        for j in range(len(u)+1):
            # Variant: len(u)+1 - j
            if i == 0 and j == 0:
                DP[i][j] = R['-']['-']

            elif i == 0:
                DP[i][j] = R[u[j-1]]['-'] + DP[i][j-1]

            elif j == 0:
                DP[i][j] = R['-'][r[i-1]] + DP[i-1][j]
            else:
                replace = R[u[j-1]][r[i-1]] + DP[i-1][j-1]
                insert = R['-'][r[i-1]] + DP[i-1][j]
                remove = R[u[j-1]]['-'] + DP[i][j-1]
                DP[i][j] = min(replace, insert, remove)

    return DP[len(r)][len(u)]

# Solution to Task C:
def min_difference_align(u: str, r: str,
                         R: Dict[str, Dict[str, int]]) -> Tuple[int, str, str]:
    """
    Sig:  str, str, Dict[str, Dict[str, int]] -> Tuple[int, str, str]
    Pre:  For all characters c in u and k in r,
          then R[c][k] exists, and R[k][c] exists.
    Post: None
    Ex:   Let R be the resemblance matrix where every change and skip
          costs 1
          min_difference_align("dinamck", "dynamic", R) -->
                                    3, "dinam-ck", "dynamic-"
    """

    #u is x-axis and r is y-axix
    # [Value, Direction] 1=Diagonal=Replace, 2=Up=Insert, 3=Left=Remove
    DP = [ [ [None, None] for i in range(len(u)+1) ] for j in range(len(r)+1) ]
    # Inner loop variant: len(u)+1 - i
    # Outer loop variant: len(r)+1 - j
    res_u = ""
    res_r = ""
    for i in range(len(r)+1):
        # Variant: len(r)+1 - i
        for j in range(len(u)+1):
            # Variant: len(u)+1 - j
            if i == 0 and j == 0:
                DP[i][j][0] = R['-']['-']

            elif i == 0:
                DP[i][j][0] = R[u[j-1]]['-'] + DP[i][j-1][0]
                DP[i][j][1] = 3

            elif j == 0:
                DP[i][j][0] = R['-'][r[i-1]] + DP[i-1][j][0]
                DP[i][j][1] = 2

            else:
                replace = R[u[j-1]][r[i-1]] + DP[i-1][j-1][0]
                insert = R['-'][r[i-1]] + DP[i-1][j][0]
                remove = R[u[j-1]]['-'] + DP[i][j-1][0]

                operations = [replace, insert, remove]
                min_cost = min(operations)
                min_operation = operations.index(min_cost)

                DP[i][j][0] = min_cost
                DP[i][j][1] = min_operation+1

    current = [len(r), len(u)]
    for k in range(len(u)+len(r)+1):
        # Variant: len(u)+len(r)+1 - k
        if current[0] == 0 and current[1] == 0:
            break

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

    return (DP[len(r)][len(u)][0], res_u, res_r)

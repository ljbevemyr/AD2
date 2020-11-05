#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 1, Problem 1: Weightlifting

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
from src.weightlifting_data import data  # noqa
from typing import List, Set  # noqa
import unittest  # noqa
# If you need to log information during tests, execution, or both,
# then you can use this library:
# Basic example:
#   logger = logging.getLogger("put name here")
#   a = 5
#   logger.debug(f"a = {a}")
import logging  # noqa

__all__ = ['weightlifting', 'weightlifting_subset']

def wl_extended(P: List[int], idx: int, w: int, mem: dict, subSet: set()) -> bool:
    '''
    Sig:  P: List[int], idx: int, w: int, mem: dict, subSet: set()) -> bool
    Pre:  mem and subSet must be empty. idx must be the last index in P.
    Post: mem will contain bools for all visited values in P,
          for each respective weight. subSet will contain a set
          of values which sum up to w.
    Ex:   P: [7, 40, 9, 24, 95]
          idx: 4
          w: 102
          mem: {}
          subSet: {}
          wl_extended(P, 4, 102, {}) = True (subSet will contain {7, 95})
    '''
    if w == 0:
        return True
    if idx < 0 or w < 0:
        return False

    key = (idx, w)
    new_weight = w - P[idx]

    if key not in mem:
        include = wl_extended(P, idx-1, new_weight, mem, subSet)
        if include:
            subSet.add(P[idx])
        else:
            exclude = wl_extended(P, idx-1, w, mem, subSet)

        mem[key] = include or exclude

    return mem[key]


def wl(P: List[int], idx: int, w: int, mem: dict) -> bool:
    '''
    Sig:  (P: List[int], idx: int, w: int, mem: dict) -> bool
    Pre:  mem must be empty. idx must be the last index in P.
    Post: mem will contain bools for all visited values in P,
          for each respective weight.
    Ex:   P: [7, 40, 9, 24, 95]
          idx: 4
          w: 102
          mem: {}
          wl(P, 4, 102, {}) = True
    '''
    if w == 0:
        return True
    if idx < 0 or w < 0:
        return False

    key = (idx, w)
    new_weight = w - P[idx]

    if key not in mem:
        include = wl(P, idx-1, new_weight, mem)
        exclude = wl(P, idx-1, w, mem)

        mem[key] = include or exclude

    return mem[key]


def weightlifting(P: Set[int], weight: int) -> bool:
    '''
    Sig:  Set[int], int -> bool
    Pre:
    Post:
    Ex:   P = {2, 32, 234, 35, 12332, 1, 7, 56}
          weightlifting(P, 299) = True
          weightlifting(P, 11) = False
    '''
    plate_list = list(P)
    mem = {}
    return wl(list(P), len(P)-1, weight, mem)


def weightlifting_subset(P: Set[int], weight: int) -> Set[int]:
    '''
    Sig:  Set[int], int -> Set[int]
    Pre:
    Post:
    Ex:   P = {2, 32, 234, 35, 12332, 1, 7, 56}
          weightlifting_subset(P, 299) = {56, 7, 234, 2}
          weightlifting_subset(P, 11) = {}
    '''
    subSet = set()

    if weight == 0 or len(P) == 0:
        return subSet
    mem = {}

    wl_extended(list(P), len(P)-1, weight, mem, subSet)

    return subSet

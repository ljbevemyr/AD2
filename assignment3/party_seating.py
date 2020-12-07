#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 3, Problem 2: Party Seating

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
from typing import *  # noqa
import unittest  # noqa
from src.party_seating_data import data  # noqa
import logging  # noqa

__all__ = ['party']


def party(known: List[List[int]]) -> Tuple[bool, List[int], List[int]]:
    """
    Sig:  List[List[int]] -> Tuple[bool, List[int], List[int]]
    Pre:
    Post:
    Ex:   party([[1, 2], [0], [0]]) = True, [0], [1, 2]
    """
    if (len(known) == 0):
        return False, [], []

    table1 = set()
    table2 = set()
    stack = set()
    notHandledPersons = set()
    for i in range(len(known)):
        # Variant: len(known)-i
        notHandledPersons.add(i)

    for i in range(len(known)):
        # Variant: len(known)-i
        table1Free = True
        table2Free = True
        if (len(stack) == 0):
            stack.add(notHandledPersons.pop())
        person = stack.pop()
        friends = known[person]
        for friend in friends:
            # Variant: len(friends)-friends.index(friends)
            if friend in table1:
                table1Free = False
            elif friend in table2:
                table2Free = False
            if (friend not in table1 and friend not in table2 and friend not in stack):
                stack.add(friend)
                notHandledPersons.remove(friend)

        if table1Free:
            table1.add(person)
        elif table2Free:
            table2.add(person)
        else:
            return False, [], []

    return True, table1, table2

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524

"""

__author__ = "Gahan Saraiya"

DEBUG = True
DEBUG = False


def debug_log(*args, **kwargs):
    override = kwargs.get('override', False)
    sep = kwargs.get("sep", " ")
    end = kwargs.get("sep", "\n")
    if DEBUG or override:
        print(*args, sep=sep, end=end)


def calculate_utilization(process_lis):
    """
    :param process_lis: list of pairs of [computation, period] for each process
    :return: processor utilization
    """
    return sum([process_lis[i][0] / process_lis[i][1] for i in range(len(process_lis))])


def calculate_upper_bound(n):
    return n * ((2 ** (1 / float(n))) - 1)

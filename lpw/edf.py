#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524

Perform Comparative analysis of RM and EDF under Transient overload
"""

__author__ = "Gahan Saraiya"

from utility import *


def is_schedulable(process_lis):
    current_task_utilization = calculate_utilization(process_lis)
    if current_task_utilization <= 1:
        return True, process_lis
    else:
        return False, process_lis

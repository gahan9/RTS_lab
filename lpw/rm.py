#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524

Perform Comparative analysis of RM and EDF under Transient overload
"""

__author__ = "Gahan Saraiya"


import math
from utility import *


def is_schedulable(processes):
    # print(compute(processes))
    current_task_utilization = calculate_utilization(processes)
    number_of_process = len(processes)
    upper_bound = calculate_upper_bound(number_of_process)
    if current_task_utilization <= upper_bound:
        debug_log("[SUCCESS] Processes are schedulable")
        return True, processes
    elif current_task_utilization > 1:
        return False, processes
    else:
        debug_log("Scheduling set of {} processes: {}".format(number_of_process, processes))
        # calculate upper bound for schedulable tasks  n * (2^(1/n) - 1)
        # find out if RM schedulable for utilization 0.69 to 1
        schedule_failed = False
        failed_task = None
        schedule_success = True  # set schedulable status
        for task in range(1, number_of_process):
            max_computation_time = sum([processes[j][0] for j in range(task + 1)])
            _computation_time = processes[task][0]
            _deadline = processes[task][1]
            while True:
                i = task - 1
                while i >= 0:
                    _computation_time += math.ceil(max_computation_time / float(processes[i][1]) * processes[i][0])
                    i -= 1
                if _computation_time > _deadline:
                    schedule_failed = True
                    failed_task = task
                    break
                if _computation_time == max_computation_time:
                    break
                else:
                    max_computation_time = _computation_time
                    _computation_time = _deadline
            if schedule_failed:
                debug_log("[FAILURE] Processes are not schedulable since processes {} can't meet deadline".format(
                    processes[failed_task][3]))
                schedule_success = False
                if processes[-1][2] == 0:
                    del processes[-1]
                    schedule_success, processes = is_schedulable(processes)
                else:
                    debug_log("[ULTIMATE-FAILURE] Task set is not schedulable!!")
                    return False, processes
                break
        return schedule_success, processes


def compute(process_lis):
    max_period = max(process_lis, key=lambda x: x[1])[1]
    for i in range(max_period):
        for i in process_lis:
            pass

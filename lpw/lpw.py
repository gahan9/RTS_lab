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
import rm
import edf

p = 0


def initialize():
    no_of_process = int(input("Enter No. of processes: "))
    print("\nNumber of processes = ", no_of_process)
    print("Enter Execution time and Period of Processes")
    processes = [list(map(int, input().split())) for i in range(no_of_process)]
    processes.sort(key=lambda x: x[1])  # sort process by period
    print(["computation", "period", "is_critical?"])
    [print(i[:3]) for i in processes]
    return no_of_process, processes


def transient_overload(process_lis, iteration=0, method="divide"):
    if iteration > 1:
        print("Not Schedulable")
        return process_lis
    debug_log("Applying Transient Overload to Process set: {}".format(process_lis))
    iteration += 1
    if method == "divide":
        # Modify deadline and computation time by dividing non critical task
        # Get minimum of non critical task
        min_of_non_critical = min([i[1] for i in process_lis if i[2] == 0])
        debug_log(">>> Min of non critical task period -- {}".format(min_of_non_critical))
        # Modify critical task
        for task in process_lis:
            if task[2] == 1 and task[1] >= min_of_non_critical:
                k = 2
                while task[1] / k >= min_of_non_critical:
                    k += 1
                    task[1] = task[1] / k
                    task[0] = task[0] / k
    elif method == "multiply":
        # Modify deadline of non critical task by factor of k
        # get max period of non critical task
        max_of_critical = max([i[1] for i in process_lis if i[2] == 1])
        debug_log(">>> Max of critical task period -- {}".format(max_of_critical))
        # task set modification
        processes_to_add = []
        for task in process_lis:
            if task[2] == 0 and task[1] <= max_of_critical:
                k = 2
                while task[1] * k <= max_of_critical:
                    k += 1
                task[1] = task[1] * k
                for i in range(k-1):
                    processes_to_add.append(task)
                # print(">>>", task)
            debug_log("processes_to_add", processes_to_add)
        process_lis += processes_to_add
    # print(process_lis)
    process_lis.sort(key=lambda x: x[1])
    debug_log("Updated Process set: {}".format(process_lis))
    return process_lis


if __name__ == "__main__":
    number_of_process, processes = initialize()
    number_of_critical_tasks = len([i for i in processes if i[2] == 1])
    number_of_non_critical_tasks = number_of_process - number_of_critical_tasks
    utilization = calculate_utilization(processes)
    status = False
    process_set = processes
    print("Initial Utilization: {}".format(utilization))
    print("{:^17}{:^17}{:^17}{:^17}{:^17}{:^17}{:^17}{:^17}".format("Algorithm",
                                                                    "Total", "Criticals",
                                                                    "Transient",
                                                                    "Scheduled?", "Critical[s]", "NonCritical[s]",
                                                                    "Utilization"))
    method = "divide"
    method = "multiply"
    for algorithm in ["RM", "EDF"]:
        print("{:^17}{:^17}{:^17}".format(algorithm, number_of_process, number_of_critical_tasks), end="")
        # print("--------------------------------------------")
        # print("Analyzing {}".format(algorithm))
        # print("============================================")
        schedule_function = rm.is_schedulable if algorithm == "RM" else edf.is_schedulable
        if utilization > 1:
            debug_log("All Tasks are not schedulable as utilization > 1")
            # filter out the critical tasks
            critical_task_set = [i for i in processes if i[2] == 1]
            if calculate_utilization(critical_task_set) > 1:
                debug_log("All Critical tasks can not be scheduled")
            else:
                print("{:^17}".format(method), end="")
                updated_process = transient_overload(processes, method=method)
                status, process_set = schedule_function(updated_process)
                process_set = sorted(process_set, key=lambda x: x[2], reverse=True)
                while not status and len(process_set) > 1:
                    popped_task = process_set.pop()
                    if popped_task[2] == 1:
                        status = False
                        break
                    status, process_set = schedule_function(process_set)
        elif 0.69 < utilization <= 1 and algorithm == "RM":
            status, process_set = schedule_function(processes)
            if not status:
                print("{:^17}".format(method), end="")
                updated_process = transient_overload(process_set, method=method)
                # updated_process = transient_overload(process_set, method="divide")
                debug_log("----------- Updated Process List -----------", override=False)
                debug_log(*updated_process, sep="\n", override=False)
                debug_log("--------------------------------------------")
                status, process_set = schedule_function(updated_process)
        else:
            debug_log("Tasks are guaranteed to be scheduled")
            status = True
            process_set = processes
        if status:
            critical_task_scheduled = len([i for i in process_set if i[2] == 1])
            non_critical_task_scheduled = len([i for i in process_set if i[2] == 0])
            # print("[{}] Scheduled {} critical tasks\nand\n{} non critical tasks".format(
            #     algorithm,
            #     critical_task_scheduled,
            #     non_critical_task_scheduled)
            # )
            print("{:^17}{:^17}{:^17}{:^17}".format("Yes" if status else "No",
                                                    critical_task_scheduled,
                                                    non_critical_task_scheduled,
                                                    calculate_utilization(process_set)))
        # print("-*"*25)
        else:
            print("{:^17}{:^17}{:^17}{:^17}".format("Yes" if status else "No", "N/A", "N/A", "N/A", "N/A"))

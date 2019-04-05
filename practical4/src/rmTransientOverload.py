#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524

Implementing Rate Monotonic Algorithm with Transient Overload

Goal:- Change period of critical task so that RM consider it as higher priority
    over non-critical
"""
__author__ = "Gahan Saraiya"

import math

p = 0


def pretty_print(processes, n):
    execution = [processes[i][0] for i in range(n)]
    _lcm = max((map(lambda x: x[1], processes)))
    _lcm = math.ceil(_lcm)
    while True:
        ind = 0
        for j in range(n):
            if _lcm % processes[j][1] == 0:
                ind += 1
        if ind == n:
            break
        else:
            _lcm += 1
    Result = []
    for i in range(0, _lcm):
        if i != 0:
            for k in range(0, n):
                if i % processes[k][1] == 0:
                    execution[k] = processes[k][0]
        ind = 0
        for j in range(n):
            if execution[j] != 0:
                execution[j] = execution[j] - 1
                # Result.append(j + 1)
                Result.append(processes[j][3])
                ind = 1
                break
        if ind == 0:
            Result.append(-1)

    print("{0}\n{1}\n{0}".format('-' * 25, '|\ttime\t task\t|'))
    for i in range(0, _lcm):
        if Result[i] != -1:
            print('|\t{}-{} \t {:^6}\t|'.format(i, i+1, Result[i]))
            # print("%d - %d: %d" % (i, i + 1, Result[i]))
        else:
            print('|\t{}-{}\t {:^6}\t|'.format(i, i+1, "idle"))
    print('-'*25)
    return


def initialize():
    no_of_process = int(input("Enter No. of processes: "))
    print("\nNumber of processes = ", no_of_process)
    print("Enter Execution time and Period of Processes")
    processes = [list(map(int, input().split())) for i in range(no_of_process)]
    processes.sort(key=lambda x: x[1])  # sort process by period
    print(["computation", "period"])
    [print(i) for i in processes]
    return no_of_process, processes


def calculate_utilization(process_lis):
    """
    :param process_lis: list of pairs of [computation, period] for each process
    :return: processor utilization
    """
    return sum([process_lis[i][0] / process_lis[i][1] for i in range(len(process_lis))])


def calculate_upper_bound(n):
    return n * ((2 ** (1 / float(n))) - 1)


def scheduler(processes, iteration=0):
    # if iteration > 1:
    #     print("Not schedulable")
    #     return False
    # iteration += 1
    number_of_process = len(processes)
    print("Scheduling set of {} processes: {}".format(number_of_process, processes))
    # calculate upper bound for schedulable tasks  n * (2^(1/n) - 1)
    upper_bound = calculate_upper_bound(number_of_process)
    if utilization <= upper_bound:
        # i.e. utilization <= 0.69
        print("processes are schedulable")
        pretty_print(processes, number_of_process)
    else:
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
                print("[FAILURE] Processes are not schedulable since processes {} can't meet deadline".format(processes[failed_task][3]))
                schedule_success = False
                if processes[-1][2] == 0:
                    del processes[-1]
                    scheduler(processes)
                else:
                    print("[ULTIMATE-FAILURE] Task set is not schedulable!!")
                    return False
                break
        if schedule_success:
            print("[SUCCESS] Processes are schedulable")
            pretty_print(processes, number_of_process)
            return True


def transient_overload(process_lis, iteration=0, method="divide"):
    if iteration > 1:
        print("Not Schedulable")
        return process_lis
    print("Applying Transient Overload to Process set: {}".format(process_lis))
    iteration += 1
    if method == "divide":
        # Modify deadline and computation time by dividing non critical task
        # Get minimum of non critical task
        min_of_non_critical = min([i[1] for i in process_lis if i[2] == 0])
        print(">>> Min of non critical task period -- {}".format(min_of_non_critical))
        # Modify critical task
        for task in process_lis:
            if task[2] == 1 and task[1] >= min_of_non_critical:
                while task[1] >= min_of_non_critical:
                    task[1] = task[1] / 2
                    task[0] = task[0] / 2
    elif method == "multiply":
        # Modify deadline of non critical task by factor of k
        # get max period of non critical task
        max_of_critical = max([i[1] for i in process_lis if i[2] == 1])
        print(">>> Max of critical task period -- {}".format(max_of_critical))
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
        print("processes_to_add", processes_to_add)
        process_lis += processes_to_add
    # print(process_lis)
    process_lis.sort(key=lambda x: x[1])
    print("Updated Process set: {}".format(process_lis))
    return process_lis


if __name__ == "__main__":
    number_of_process, processes = initialize()
    utilization = calculate_utilization(processes)
    print("Utilization: {}".format(utilization))
    if utilization > 1:
        print("All Tasks are not schedulable with RMA as utilization > 1")
        # here comes the part of Transient Overload
        critical_task_set = [i for i in processes if i[2] == 1]
        if calculate_utilization(critical_task_set) > 1:
            print("All Critical tasks can not be scheduled with RMA")
        # else:
        #     # task modification
        #     updated_process = transient_overload(processes)
        #     scheduler(updated_process)
    elif 0.69 < utilization <= 1:
        if not scheduler(processes):
            updated_process = transient_overload(processes, method="multiply")
            # updated_process = transient_overload(processes, method="divide")
            print("----------- Updated Process List -----------")
            print(*updated_process, sep="\n")
            print("--------------------------------------------")
            scheduler(updated_process)
    else:
        print("Tasks are guaranteed to be scheduled")
        pretty_print(processes, 2)

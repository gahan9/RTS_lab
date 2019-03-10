#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524

"""
__author__ = "Gahan Saraiya"

import math

p = 0


def pretty_print(processes, n):
    execution = [processes[i][0] for i in range(n)]
    _lcm = max((map(lambda x: x[1], processes)))
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
                Result.append(j + 1)
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
            print('|\t{}-{}\t {:^6}\t|'.format(i, i+1, "Idle"))
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


calculate_upper_bound = lambda n: n * ((2 ** (1 / float(n))) - 1)

if __name__ == "__main__":
    number_of_process, processes = initialize()
    utilization = calculate_utilization(processes)
    print("Utilisation: {}".format(utilization))
    if utilization > 1:
        print("Tasks are not schedulable with RM")
    elif utilization <= 1:
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
                    print("Processes are not schedulable since processes {} can't meet deadline".format(failed_task))
                    schedule_success = 0
                    break
            if schedule_success == 1:
                print("processes are schedulable")
                pretty_print(processes, number_of_process)

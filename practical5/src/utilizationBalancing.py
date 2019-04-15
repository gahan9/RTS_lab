#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524

Implementation of Utilization Balancing Algorithm for Multiprocessor Task Allocation
"""
import math

__author__ = "Gahan Saraiya"

__doc__ = """Utilization Balancing Algorithm for Multiprocessor Task Allocation
---
- Algorithm maintains the tasks in increasing/decreasing order of their utilization in a list (as per defined)
- removes tasks one by one from the end of the list and allocates to least utilized processor each time.
"""
import random

NUMBER_OF_PROCESSORS = random.randint(20, 100)
NUMBER_OF_TASKS = random.randint(NUMBER_OF_PROCESSORS, NUMBER_OF_PROCESSORS*3)
HIGHEST_UTILIZATION_FIRST = False
METHOD = "lowest utilization task assigned" if not HIGHEST_UTILIZATION_FIRST else "highest utilization task assigned"

def initialize_processors(no_of_processors):
    """
    Initialize dictionary of number of processor
    :param no_of_processors: number of processors
    :return: dictionary of all processors initialized to zero load
    {
    <Processor-id>: [<processor-utilization>, [<list-of-tasks>]]
    }
    """
    return {"P{:0>3}".format(i): [0.0, []] for i in range(no_of_processors)}


def generate_task_set(no_of_tasks, **kwargs):
    """
    Generate task list
    :param no_of_tasks: number of task to be generated
    :return: dictionary of task list
    {
    <task-id>: [<execution-time>, <periodicity>, <task-utilization>]
    }
    """
    tasks = {}
    _total_utilization = 0.0
    display = kwargs.get('display', False)
    padding = kwargs.get('padding', 15)
    _diff = kwargs.get('diff', 15)
    _max = kwargs.get('max_bound', 60)
    execution_upper_bound = kwargs.get('execution_upper_bound', 20)
    if display:
        print("|{0}|\n|{1:^{5}}{2:^{5}}{3:^{5}}{4:^{5}}|\n|{0}|".format('-' * 4 * padding, 'Task-id', 'Execution', 'Periodicity', 'Utilization', padding))
    for i in range(no_of_tasks):
        task_id = "T{:0>3}".format(i)
        execution_time = random.randint(1, execution_upper_bound)
        periodicity = random.randint(execution_time+_diff, execution_time+_diff+_max)
        task_utilization = execution_time / periodicity
        _total_utilization += task_utilization
        tasks[task_id] = [execution_time, periodicity, task_utilization]
        if display:
            print("{0}{1:^{5}}{2:^{5}}{3:^{5}}{4:^{5}.10f}{0}".format('|', task_id, execution_time, periodicity, task_utilization, padding))
    if display:
        print("-{}-".format("-"*4*padding))
    return tasks, _total_utilization


def get_processor_to_assign(processor_set):
    """
    Pick lowest utilized processor
    :param processor_set: processor utilization set
    :return: id/dict key of lowest utilized processor
    """
    return min(processor_set, key=lambda x: processor_set[x][0])


def pretty_print(processor_set, padding=15):
    print("{0}\n{1:<{4}}{2:<{4}}{3:<{4}}\n{0}".format('-'*3*padding, 'Processor-id', 'Utilization', 'Task-list', padding))
    for p in processor_set:
        utilization = processor_set[p][0]
        task_lis = ', '.join(processor_set[p][1])
        print("{0:<{3}}{1:<{3}.10f}{2:<{3}}".format(p, utilization, task_lis, padding))


def analyze(processor_set):
    total_processors = len(processor_set)
    utilizations = [val[0] for key, val in processor_set.items()]
    utilization_sum = sum(utilizations)
    mean_utilization = utilization_sum / total_processors
    utilization_variance = sum([(i-mean_utilization)**2 for i in utilizations]) / total_processors
    utilization_std_deviation = utilization_variance ** 0.5
    coefficient_of_variation = (utilization_std_deviation / mean_utilization) * 100
    print("="*50)
    print("METHOD: {}".format(METHOD))
    print("Total Processors: {}".format(total_processors))
    print("Mean: {}".format(mean_utilization))
    print("Variance: {}".format(utilization_variance))
    print("Standard Deviation: {}".format(utilization_std_deviation))
    print("Coefficient of Variation: {}".format(coefficient_of_variation))
    print("="*50)

if __name__ == "__main__":
    task_set, total_utilization = generate_task_set(NUMBER_OF_TASKS)
    required_processors = math.ceil(total_utilization)
    print("Required Processors: {}".format(required_processors) +
          "\nAvailable Processors: {}".format(NUMBER_OF_PROCESSORS) +
          "\nCalculated Utilization: {}".format(total_utilization)
          )
    if required_processors > NUMBER_OF_PROCESSORS:
        print("Insufficient processors to assign task for scheduling")
        exit(1)
    for i in ["increasing", "decreasing", "random"]:
        processor_utilization = initialize_processors(NUMBER_OF_PROCESSORS)
        METHOD = i
        if i == "increasing":
            ordered_task_list = sorted(task_set, key=lambda x: task_set[x][2])
        elif i == "decreasing":
            ordered_task_list = sorted(task_set, key=lambda x: task_set[x][2], reverse=True)
        else:
            ordered_task_list = sorted(task_set, key=lambda x: task_set[x][2])
            random.shuffle(ordered_task_list)
        while ordered_task_list:
            task_to_assign = ordered_task_list.pop(0)  # pop task from end of the list (lowest utilized task if HIGHEST_UTILIZATION_FIRST is False)
            processor = get_processor_to_assign(processor_utilization)
            processor_utilization[processor][0] += task_set[task_to_assign][2]
            processor_utilization[processor][1] += [task_to_assign]
        # pretty_print(processor_utilization)
        analyze(processor_utilization)
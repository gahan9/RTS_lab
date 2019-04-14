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

NUMBER_OF_PROCESSORS = 10
NUMBER_OF_TASKS = 20
HIGHEST_UTILIZATION_FIRST = False


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
    display = kwargs.get('display', True)
    padding = kwargs.get('padding', 15)
    if display:
        print("|{0}|\n|{1:^{5}}{2:^{5}}{3:^{5}}{4:^{5}}|\n|{0}|".format('-' * 4 * padding, 'Task-id', 'Execution', 'Periodicity', 'Utilization', padding))
    for i in range(no_of_tasks):
        task_id = "T{:0>3}".format(i)
        execution_time = random.randint(1, 20)
        periodicity = random.randint(execution_time+2, execution_time+30)
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


if __name__ == "__main__":
    task_set, total_utilization = generate_task_set(NUMBER_OF_TASKS)
    required_processors = math.ceil(total_utilization)
    print("Required Processors: {}".format(required_processors) +
          "\nAvailable Processors: {}".format(NUMBER_OF_PROCESSORS)
          )
    if required_processors > NUMBER_OF_PROCESSORS:
        print("Insufficient processors to assign task for scheduling")
        exit(1)
    processor_utilization = initialize_processors(NUMBER_OF_PROCESSORS)
    # sort keys of task by utilization
    # descending if HIGHEST_UTILIZATION_FIRST is False
    # ascending if HIGHEST_UTILIZATION_FIRST is True
    ordered_task_list = sorted(task_set, key=lambda x: task_set[x][2], reverse=not HIGHEST_UTILIZATION_FIRST)
    while ordered_task_list:
        task_to_assign = ordered_task_list.pop()  # pop task from end of the list (lowest utilized task if HIGHEST_UTILIZATION_FIRST is False)
        processor = get_processor_to_assign(processor_utilization)
        processor_utilization[processor][0] += task_set[task_to_assign][2]
        processor_utilization[processor][1] += [task_to_assign]
    pretty_print(processor_utilization)

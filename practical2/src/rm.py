#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524

Implementing Rate Monotonic Scheduling Algorithm
"""
__author__ = "Gahan Saraiya"
from sys import *
from functools import reduce
import math
import pandas as pd


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def lcm(a, b):
    return a * b / gcd(a, b)


def LCM(list):
    return math.ceil(reduce(lcm, list))


def load_tasks(task_file):
    f = open(task_file)
    data = f.read()
    f.close()

    data = data.split('\n')
    tasks = {}
    period_list = []
    for i in data[1:]:
        i = i.split(',')
        if len(i) > 2:
            tasks[i[0]] = {}
            tasks[i[0]]['wcet'] = int(i[1])
            tasks[i[0]]['period'] = int(i[2])
            period_list.append(int(i[2]))
    lcm_period = LCM(period_list)
    # insert idle task
    tasks['idle'] = {'wcet': lcm_period, 'period': lcm_period + 1}
    return tasks, lcm_period


def scheduler(tasks, D):
    queue = list(tasks.keys())  # initialize task queue
    schedule = []
    curr = ''  # current task
    prev = ''  # previous task
    tmp = {}
    for task in tasks.keys():
        tmp[task] = {}  # temporary data for each task
        tmp[task]['deadline'] = tasks[task]['period']
        tmp[task]['executed'] = 0

    # start scheduling...
    # proceed by one timestamp to handle preemption
    for time in range(D):
        # insert new tasks into the queue
        for t in tmp.keys():
            if time == tmp[t]['deadline']:
                if tasks[t]['wcet'] > tmp[t]['executed']:
                    print('Scheduling Failed at %d' % time)
                    exit(1)
                else:
                    tmp[t]['deadline'] += tasks[t]['period']
                    tmp[t]['executed'] = 0
                    queue.append(t)
        # select next task to be scheduled
        _min = D * 2
        for task in queue:
            if tmp[task]['deadline'] < _min:
                _min = tmp[task]['deadline']
                curr = task
        tmp[curr]['executed'] += 1
        print(time, queue, curr)

        # de queue the execution-completed task
        if tmp[curr]['executed'] == tasks[curr]['wcet']:
            for i in range(len(queue)):
                if curr == queue[i]:
                    del queue[i]
                    break

        # record to the schedule trace
        if prev != curr:
            if prev in queue and prev != 'idle':  # previous task is preempted..
                s = schedule.pop()
                schedule.append([s[0], s[1], '*'])
            schedule.append([time, curr])
        prev = curr

    # check correctness
    k = {}
    for i in tasks.keys():
        k[i] = 0
    for s in schedule:
        if len(s) == 2:  # count un preempted tasks
            k[s[1]] += 1
    print(k)
    return schedule


def print_schedule(s):
    print('-' * 25)
    print('|\ttime\ttask\t|')
    print('-' * 25)
    for i in range(len(s)):
        t = s.pop(0)
        if len(t) == 2:
            print('|\t%d\t%s\t|' % (t[0], t[1].strip()))
        else:
            print('|\t%d\t%s\t|' % (t[0], t[1].strip() + t[2].strip()))
    print('-'*25)


if __name__ == '__main__':
    if len(argv) < 2:
        print('Usage: python %s input_file' % argv[0])
        exit(1)
    a, b = load_tasks(argv[1])
    s = scheduler(a, b)
    print_schedule(s)

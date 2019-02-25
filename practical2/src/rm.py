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


class RateMonotonic(object):
    def __init__(self, task_file):
        self.task_file = task_file
        self.data = open(self.task_file).read().split("\n")
        self.tasks, self.lcm_period = self.load_tasks()
        self.schedule = []

    def gcd(self, a, b):
        return a if b == 0 else self.gcd(b, a % b)

    def lcm(self, a, b):
        return a * b // self.gcd(a, b)

    def LCM(self, lis):
        return math.ceil(reduce(self.lcm, lis))

    def load_tasks(self):
        tasks = {}
        period_list = []
        for i in self.data[1:]:  # skip header
            i = i.split(',')
            if len(i) > 2:
                tasks[i[0]] = {
                    'computation': int(i[1]),
                    'period': int(i[2])
                }
                period_list.append(int(i[2]))
        lcm_period = self.LCM(period_list)
        # insert idle task -- in terms of CPU non utilized...
        tasks['idle'] = {
            'computation': lcm_period,
            'period': lcm_period + 1
        }
        return tasks, lcm_period

    def scheduler(self):
        queue = list(self.tasks.keys())  # initialize task queue
        curr = ''  # current task
        prev = ''  # previous task
        tmp = {}
        for task in self.tasks.keys():
            tmp[task] = {}  # temporary data for each task
            tmp[task]['deadline'] = self.tasks[task]['period']
            tmp[task]['executed'] = 0

        # start scheduling...
        # proceed by one timestamp to handle preemption
        for time in range(self.lcm_period):
            # insert new tasks into the queue
            for t in tmp.keys():
                if time == tmp[t]['deadline']:
                    if self.tasks[t]['computation'] > tmp[t]['executed']:
                        print('Scheduling Failed at %d' % time)
                        exit(1)
                    else:
                        tmp[t]['deadline'] += self.tasks[t]['period']
                        tmp[t]['executed'] = 0
                        queue.append(t)
            # select next task to be scheduled
            _min = self.lcm_period * 2
            for task in queue:
                if tmp[task]['deadline'] < _min:
                    _min = tmp[task]['deadline']
                    curr = task
            tmp[curr]['executed'] += 1
            print(time, queue, curr)

            # de queue the execution-completed task
            if tmp[curr]['executed'] == self.tasks[curr]['computation']:
                for i in range(len(queue)):
                    if curr == queue[i]:
                        del queue[i]
                        break

            # record to the schedule trace
            if prev != curr:
                if prev in queue and prev != 'idle':  # previous task is preempted..
                    s = self.schedule.pop()
                    self.schedule.append([s[0], s[1], '*'])
                self.schedule.append([time, curr])
            prev = curr

        # check correctness
        k = {}
        for i in self.tasks.keys():
            k[i] = 0
        for s in self.schedule:
            if len(s) == 2:  # count un preempted tasks
                k[s[1]] += 1
        # print(k)
        return self.schedule

    @staticmethod
    def pretty_print(schedule):
        print("{0}\n{1}\n{0}".format('-' * 25, '|\ttime\ttask\t|'))
        for i in range(len(schedule)):
            t = schedule.pop(0)
            if len(t) == 2:
                print('|\t{}\t{}\t|'.format(t[0], t[1].strip()))
            else:
                print('|\t{}\t{}\t|'.format(t[0], t[1].strip() + t[2].strip()))
        print('-'*25)


if __name__ == '__main__':
    if len(argv) < 2:
        print('Usage: python {} <input-file>'.format(argv[0]))
        exit(1)
    rm = RateMonotonic(argv[1])
    schedule = rm.scheduler()
    rm.pretty_print(schedule)

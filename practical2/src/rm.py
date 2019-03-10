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
    def __init__(self, task_file, mode="NORMAL"):
        self.task_file = task_file
        self.data = open(self.task_file).read().split("\n")
        self.tasks, self.lcm_period = self.load_tasks()
        self.schedule = []
        self.mode = mode
        if self.mode == "DEBUG":
            self.task_printer()
        self.task_count_in_schedule = self.task_count()

    def task_count(self):
        _d = {}
        for key, val in self.tasks.items():
            if key != "idle":
               _d[key] = math.ceil(self.lcm_period / val['period'])
        # print(_d)
        return _d

    def task_printer(self):
        print("{}\nMax Deadline: {}".format('=' * 20, self.lcm_period))
        for i, j in self.tasks.items():
            print("{} -- {}".format(i, j))
        print('=' * 20)

    def debug(self, *args):
        if self.mode == "DEBUG":
            for i in args:
                print("[{}]: {}".format(self.mode, i))

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
                    'period': int(i[2]),
                    'deadline': int(i[2]),
                    'executed': 0
                }
                period_list.append(int(i[2]))
        lcm_period = self.LCM(period_list)
        # insert idle task -- in terms of CPU non utilized...
        tasks['idle'] = {
            'computation': lcm_period,
            'period': lcm_period + 1,
            'deadline': lcm_period + 1,
            'executed': 0
        }
        return tasks, lcm_period

    def scheduler(self):
        queue = list(self.tasks.keys())  # initialize task queue
        curr = ''  # current task
        prev = ''  # previous task
        # self.debug(self.tasks)

        # start scheduling...
        # proceed by one timestamp to handle preemption
        for time in range(int(self.lcm_period)):
            # self.debug("INITIAL STATE ==> {} \t{} \t{}".format(time, queue, curr))
            # insert new tasks into the queue
            for t in self.tasks.keys():
                # self.debug("{} == {} || {}".format(time, t, self.tasks[t]))
                if time == self.tasks[t]['deadline']:
                    if self.tasks[t]['computation'] > self.tasks[t]['executed']:
                        print('Scheduling Failed at {}'.format(time))
                        exit(1)
                    else:
                        self.tasks[t]['deadline'] += self.tasks[t]['period']
                        self.tasks[t]['executed'] = 0
                        # self.debug("TASK_DEADLINE>>> {} added to queue".format(t))
                        queue.append(t)
            # self.debug("Queue at time unit >>> {} <<< is >>> {} <<<".format(time, queue))
            # select next task to be scheduled
            _min = self.lcm_period * 2
            for task in queue:
                # self.debug("task updater---------- {}".format(task))
                # self.debug(self.tasks[task]['deadline'], _min)
                if self.tasks[task]['deadline'] <= _min:
                    _min = self.tasks[task]['deadline']
                    curr = task
            self.tasks[curr]['executed'] += 1

            # de queue the execution-completed task
            # self.debug("------", "TIME: {}".format(time), self.tasks)
            if self.tasks[curr]['executed'] == self.tasks[curr]['computation']:
                # queue.remove(curr)
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

        self.debug(self.schedule)
        # check correctness
        k = {}
        for i in self.tasks.keys():
            k[i] = 0
        # self.debug(self.task_count_in_schedule)
        for s in self.schedule:
            if s[1] != "idle":
                self.task_count_in_schedule[s[1]] = self.task_count_in_schedule[s[1]] - s[0]
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
    rm = RateMonotonic(argv[1], mode="DEBUG")
    schedule = rm.scheduler()
    rm.pretty_print(schedule)

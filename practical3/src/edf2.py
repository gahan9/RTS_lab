#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524

Implementation of EDF (Earliest Deadline First) Algorithm
"""
import math
from functools import reduce

__author__ = "Gahan Saraiya"

from sys import *


class Scheduler(object):
    def __init__(self, task_file, mode="NORMAL"):
        self.task_file = task_file
        self.data = open(self.task_file).read().split('\n')
        self.tasks, self.max_deadline = self.load_task()
        self.queue = []  # initialize task queue
        self.schedule = []  # output schedule
        self.mode = mode
        if mode == "DEBUG":
            self.task_printer()

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

    def task_printer(self):
        print("{}\nMax Deadline: {}".format('='*20, self.max_deadline))
        for i, j in self.tasks.items():
            print("{} -- {}".format(i, j))
        print('='*20)

    def load_task(self):
        tasks = {}
        max_deadline = 0
        period_lis = []
        for i in self.data:
            i = i.split(',')
            if len(i) > 3:
                if i[0].startswith('#'):
                    # to comment task and skip header
                    continue
                tasks[i[0]] = {'computation': int(i[2]),  # computation time
                               'deadline': int(i[3]),  # deadline
                               'release': int(i[1]),  # release time
                               'executed': 0}  # executed amount
                period_lis.append(int(i[3]))
                # if tasks[i[0]]['deadline'] > max_deadline:
                #     max_deadline = tasks[i[0]]['deadline']
        max_deadline = self.LCM(period_lis)
        # insert idle task
        tasks['idle'] = {'computation': max_deadline,
                         'deadline': max_deadline + 1,
                         'release': 0,
                         'executed': 0
                         }
        return tasks, max_deadline

    @staticmethod
    def pretty_print(schedule):
        print("{0}\n{1}\n{0}".format('-' * 25, '|\ttime\ttask\t|'))
        for i in range(len(schedule)):
            t = schedule.pop(0)
            if len(t) == 2:
                print('|\t%d\t%s\t|' % (t[0], t[1].strip()))
            else:
                print('|\t%d\t%s\t|' % (t[0], t[1].strip() + t[2].strip()))
        print('-' * 25)

    def get_schedule_order(self):
        return sorted(self.tasks, key=lambda x: self.tasks[x]['deadline'])

    def scheduler(self):
        self.debug("Initializing Scheduler with task set \n: {}".format(self.tasks))
        curr = ''  # current task
        prev = ''  # previous task
        time = 0
        task_order = self.get_schedule_order()
        while time <= self.max_deadline:
            # print("In a while...")
            _task = task_order.pop(0)
            # print(_task)
            self.debug(self.tasks[_task]['deadline'], time, self.tasks[_task]['deadline'] <= time)
            if self.tasks[_task]['deadline'] >= time >= self.tasks[_task]['release']:
                self.schedule.append([time, _task])
                time += self.tasks[_task]['computation']
                self.tasks[_task]['deadline'] = self.tasks[_task]['deadline'] * 2
                self.tasks[_task]['release'] = self.tasks[_task]['deadline']
                task_order = self.get_schedule_order()
            else:
                self.pretty_print(self.schedule)
                print("Scheduling failed at time - {}".format(time))
                break
        return self.schedule


if __name__ == '__main__':
    if len(argv) < 2:
        print('Usage: python {} <input-file>'.format(argv[0]))
        exit(1)
    s = Scheduler(argv[1], mode="DEBUG")
    schedule = s.scheduler()
    s.pretty_print(schedule)
    print(s.schedule)

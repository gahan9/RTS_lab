#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524

Implementation of EDF (Earliest Deadline First) Algorithm
"""

__author__ = "Gahan Saraiya"

from sys import *


class Scheduler(object):
    def __init__(self, task_file):
        self.task_file = task_file
        self.data = open(self.task_file).read().split('\n')
        self.tasks, self.max_deadline = self.load_task()
        self.queue = []  # initialize task queue
        self.schedule = []  # output schedule

    def load_task(self):
        tasks = {}
        max_deadline = 0
        for i in self.data:
            i = i.split(',')
            if len(i) > 3:
                if i[0].startswith('#'):
                    # to comment task and skip header
                    continue
                tasks[i[0]] = {'computation': int(i[3]),  # computation time
                               'deadline': int(i[2]),  # deadline
                               'release': int(i[1]),  # release time
                               'executed': 0}  # executed amount
                if tasks[i[0]]['deadline'] > max_deadline:
                    max_deadline = tasks[i[0]]['deadline']
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

    def scheduler(self):
        curr = ''  # current task
        prev = ''  # previous task

        # start scheduling...
        for time in range(self.max_deadline):
            # insert new tasks into the queue
            for t in self.tasks.keys():
                if time == self.tasks[t]['release']:
                    self.queue.append(t)
                elif time == self.tasks[t]['deadline']:
                    if self.tasks[t]['computation'] > self.tasks[t]['executed']:
                        self.pretty_print(self.schedule)
                        print('Scheduling Failed at %d!' % time)
                        exit(1)
            # select next task to be scheduled
            _min = self.max_deadline + 2
            for task in self.queue:
                if self.tasks[task]['deadline'] < _min:
                    _min = self.tasks[task]['deadline']
                    curr = task
            self.tasks[curr]['executed'] += 1
            # de-queue the completed task
            if self.tasks[curr]['executed'] == self.tasks[curr]['computation']:
                self.queue.remove(curr)
            # record to the schedule trace
            if prev != curr:
                if prev in self.queue and prev != 'idle':  # previous task is preempted..
                    self.schedule[-1].append('*')
                self.schedule.append([time, curr])
            prev = curr
        return self.schedule


if __name__ == '__main__':
    if len(argv) < 2:
        print('Usage: python {} <input-file>'.format(argv[0]))
        exit(1)
    s = Scheduler(argv[1])
    schedule = s.scheduler()
    s.pretty_print(schedule)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524

Implementation of EDF (Earliest Deadline First) Algorithm
"""

__author__ = "Gahan Saraiya"


class Scheduler(object):
    def __init__(self, processes):
        """
        processes: A dictionary in format as below:
            {
                "arrival_time": [...],
                "computation_time": [...],
                "deadline": [...]
            }
        """
        self.processes = processes
        self.current_time = 0

    def ready_state(self):
        return [i for i in range(len(processes['arrival_time'])) if processes['arrival_time'][i]<=self.current_time]

    def process_picker(self):
        processes_in_ready_queue = self.ready_state()
        
        return 

    def schedule(self):
        """Returns list of tuple process executed in order
        [(process,execution_time), ....]
        """
        return []


if __name__ == "__main__":
    processes = {
        "arrival_time": [0, 0, 2, 3, 6],
        "computation_time": [1, 2, 2, 2, 2],
        "deadline": [2, 5, 4, 10, 9]
    }
    s = Scheduler(processes)
    schedule = s.schedule()

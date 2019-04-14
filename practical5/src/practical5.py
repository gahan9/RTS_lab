import math
import random

NUMBER_OF_PROCESSORS, NUMBER_OF_TASKS = 20, 45
INCREASING_ORDER = True


def generate_task_set(jobs, min_diff=10):
    tasks = {}
    utilization = 0.0
    for i in range(1, jobs+1):
        job_id = "Task[{}]".format(i)
        ExecutionTime = random.randint(1, 20)
        Periodicity = random.randint(ExecutionTime+min_diff, ExecutionTime+min_diff+50)
        task_utilization = ExecutionTime / Periodicity
        utilization += task_utilization
        tasks[job_id] = [ExecutionTime, Periodicity, task_utilization]
    return tasks, utilization


def print_tasks(tasks, padding=15, precision=2):
    print("{0}\n{1:^{4}}{2:^{4}}{3:^{4}}\n{0}".format('='*3*padding, 'Task[i]', 'Execution[i]', 'Periodicity', padding))
    for key, val in tasks.items():
        print("{0:^{3}}{1:^{3}.{4}f}{2:^{3}}".format(key, val[0], val[1], padding, precision))
    return True


def print_result(processor_dict, padding=20, precision=8):
    print("{0}\n{1:^{4}}{2:^{4}}{3:^{4}}\n{0}".format('='*3*padding, 'Processor[i]', 'Utilization[i]', 'Tasks', padding))
    for key, val in processor_dict.items():
        utilization = val[0]
        task_lis = ', '.join(val[1])
        print("{0:^{3}}{1:^{3}.{4}f}{2:^{3}}".format(key, utilization, task_lis, padding, precision))
    return True


if __name__ == "__main__":
    task_set, utilization_of_task_set = generate_task_set(NUMBER_OF_TASKS)
    print_tasks(task_set)
    required_processors = math.ceil(utilization_of_task_set)
    processors = {"P[{}]".format(i+1): [0.0, []] for i in range(NUMBER_OF_PROCESSORS)}
    ordered_task_list = sorted(task_set, key=lambda x: task_set[x][2], reverse=not INCREASING_ORDER)
    while ordered_task_list:
        task_to_assign = ordered_task_list.pop(0)  # pop 1st element from list
        processor = min(processors, key=lambda x: processors[x][0])
        processors[processor][0] += task_set[task_to_assign][2]
        processors[processor][1] += [task_to_assign]
    print_result(processors)

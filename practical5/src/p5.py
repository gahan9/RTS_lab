import math
import random

NUMBER_OF_PROCESSORS = 10
NUMBER_OF_TASKS = 20
HIGHEST_UTILIZATION_FIRST = False

initialize_processors = lambda no_of_processors:  {"P{}".format(i): [0.0, []] for i in range(no_of_processors)}
get_processor_to_assign = lambda processor_set: min(processor_set, key=lambda x: processor_set[x][0])


def generate_task_set(no_of_jobs):
    tasks = {}
    _total_utilization = 0.0
    for i in range(no_of_jobs):
        job_id = "J{}".format(i)
        execution_time = random.randint(2, 15)
        periodicity = random.randint(execution_time+2, execution_time+22)
        task_utilization = execution_time / periodicity
        _total_utilization += task_utilization
        tasks[job_id] = [execution_time, periodicity, task_utilization]
    return tasks, _total_utilization


def printer(processor_set, padding=15):
    print("{0}\n{1:<5}{2:<{4}}{3:<{4}}\n{0}".format(' '*3*padding, 'P_i', 'U_i', 'Tasks', padding))
    for p in processor_set:
        utilization = processor_set[p][0]
        task_lis = ', '.join(processor_set[p][1])
        print("{0:<5}{1:<{3}.10f}{2:<{3}}".format(p, utilization, task_lis, padding))


task_set, total_utilization = generate_task_set(NUMBER_OF_TASKS)
required_processors = math.ceil(total_utilization)
processor_utilization = initialize_processors(NUMBER_OF_PROCESSORS)
ordered_task_list = sorted(task_set, key=lambda x: task_set[x][2], reverse=not HIGHEST_UTILIZATION_FIRST)
while ordered_task_list:
    task_to_assign = ordered_task_list.pop()  # pop task from end of the list (lowest utilized task if HIGHEST_UTILIZATION_FIRST is False)
    processor = get_processor_to_assign(processor_utilization)
    processor_utilization[processor][0] += task_set[task_to_assign][2]
    processor_utilization[processor][1] += [task_to_assign]
printer(processor_utilization)


import sys
import string
import decimal
import itertools
from collections import defaultdict, Counter
from pprint import pprint
import yaml
from constraint import *
from tabulate import tabulate
from days_parser import days_parser

class Task(object):

    def __init__(self, name, hours=1.0):
        self.name = name
        self.hours = decimal.Decimal(hours)

    def __lt__(self, other):
        return self.name < other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Task {self.name}:{self.hours}>"


def all_assigned(assignments, variables):
    return [assignments.get(v, Unassigned) for v in variables].count(Unassigned) == 0

class TotalHoursConstraint(Constraint):

    def __init__(self, minimum=13, maximum=14.75):
        self.minimum = decimal.Decimal(minimum)
        self.maximum = decimal.Decimal(maximum)

    def __call__(self, variables, domains, assignments, forwardcheck=False):
        if not all_assigned(assignments, variables):
            return True
        return self.minimum <= sum(t.hours for t in assignments) <= self.maximum

class MinPerDayConstraint(Constraint):

    def __call__(self, variables, domains, assignments, forwardcheck=False):
        if not all_assigned(assignments, variables):
            return True

        c = defaultdict(list)
        for task, choice in assignments.items():
            c[choice].append(task.hours)
        for day, hours in c.items():
            if sum(hours) < decimal.Decimal(2):
                return False
        return True


days = list(range(7))
dow = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def solve(fp):
    problem = Problem()
    day_restrictions = {}
    groups = defaultdict(list)
    tasks = []

    doc = yaml.safe_load(fp)
    total_days = days

    if "days" in doc:
        total_days = days_parser(doc["days"])
        problem.addConstraint(InSetConstraint(total_days))
    for task in doc["tasks"]:
        if "days" in task:
            task_days = days_parser(task["days"])
            day_restrictions[task["name"]] = task_days
        else:
            task_days = total_days

        for d in task_days:
            t = Task(task["name"])
            if "hours" in task:
                t.hours = decimal.Decimal(task["hours"])
            groups[t.name].append(t)
            tasks.append(t)

    problem.addVariables(tasks, days)

    for grp, _days in day_restrictions.items():
        problem.addConstraint(InSetConstraint(_days), groups[grp])

    problem.addConstraint(TotalHoursConstraint())
    problem.addConstraint(MinPerDayConstraint())

    for task_group, tasks in groups.items():
        problem.addConstraint(AllDifferentConstraint(), tasks)

    return problem.getSolution()


def draw_table(solution):
    rows = max(k for k, v in itertools.groupby(solution.values()))
    schedule = [[None for d in days] for row in range(rows)]
    hours_per_day = [0 for day in days]

    for task, day in solution.items():
        hours_per_day[day] += task.hours
        for row in range(rows):
            if schedule[row][day] is None:
                schedule[row][day] = task
                break

    schedule.append(hours_per_day)

    print(tabulate(schedule, headers=dow, tablefmt="fancy_grid"))
    print(sum(hours_per_day))


with open(sys.argv[1]) as fp:
    solution = solve(fp)
    draw_table(solution)

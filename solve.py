import string
import decimal
import itertools
from collections import defaultdict
from pprint import pprint
from constraint import *
from tabulate import tabulate

class Task(object):

    def __init__(self, name, hours=1.0):
        self.name = name
        self.hours = decimal.Decimal(hours)

    def __lt__(self, other):
        return self.name < other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)

class HoursConstraint(Constraint):

    def __init__(self, minimum=13, maximum=14.75):
        self.minimum = decimal.Decimal(minimum)
        self.maximum = decimal.Decimal(maximum)

    def __call__(self, variables, domains, assignments, forwardcheck=False):
        return self.minimum <= sum(t.hours for t in variables) <= self.maximum


days = list(range(7))
dow = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

tasks = [
    Task("Clean Mirrors", hours=0.5),
    Task("Clean Mirrors", hours=0.5),
    Task("Wet Mop Floors"),
    Task("Wet Mop Floors"),
    Task("Wet Mop Floors"),
    Task("Clean Kitchen Surfaces"),
    Task("Clean Kitchen Surfaces"),
    Task("Clean Kitchen Surfaces"),
    Task("Prepare Food for Next Day"),
    Task("Prepare Food for Next Day"),
    Task("Prepare Food for Next Day"),
    Task("Prepare Food for Next Day"),
    Task("Prepare Food for Next Day"),
    Task("Laundry"),
    Task("Laundry"),
]

groups = defaultdict(list)

for t in tasks:
    groups[t.name].append(t)


problem = Problem()
problem.addVariables(tasks, days)

problem.addConstraint(InSetConstraint([1,3,5]), groups["Laundry"])
problem.addConstraint(InSetConstraint([1,3,5]), groups["Wet Mop Floors"])
problem.addConstraint(InSetConstraint([1,3,5]), groups["Clean Mirrors"])
problem.addConstraint(InSetConstraint([1,3,5]), groups["Clean Kitchen Surfaces"])
problem.addConstraint(HoursConstraint())

for task_group, tasks in groups.items():
    problem.addConstraint(AllDifferentConstraint(), tasks)

solution = problem.getSolution()

rows = max(k for k, v in itertools.groupby(solution.values()))
schedule = [[None for d in days] for row in range(rows)]

for task, day in solution.items():
    for row in range(rows):
        if schedule[row][day] is None:
            schedule[row][day] = task
            break

print(tabulate(schedule, headers=dow, tablefmt="fancy_grid"))
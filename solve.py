import string
import decimal
import itertools
from collections import defaultdict, Counter
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

def days_apart(distance):
    def _f(*args):
        return sum(args) / len(args) >= distance
    return _f

problem = Problem()
problem.addVariables(tasks, days)

problem.addConstraint(InSetConstraint([1,2,3,4,5]))
problem.addConstraint(InSetConstraint([1,3,5]), groups["Laundry"])
problem.addConstraint(TotalHoursConstraint())
problem.addConstraint(MinPerDayConstraint())
problem.addConstraint(FunctionConstraint(days_apart(2)), groups["Laundry"])
problem.addConstraint(FunctionConstraint(days_apart(2)), groups["Clean Kitchen Surfaces"])
problem.addConstraint(FunctionConstraint(days_apart(3)), groups["Wet Mop Floors"])

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

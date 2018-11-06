import sys
from constraint import Problem, InSetConstraint, MaxSumConstraint, Unassigned
from calendar import TextCalendar

import yaml

with open(sys.argv[1]) as fp:
    config = yaml.safe_load(fp)

day_map = {"Sa": 5, "Su": 6, "Mo": 0, "Tu": 1, "We": 2, "Th": 3, "Fr": 4}
regular = {day_map[k]: v for k, v in config.get("regular", {}).items()}
special = config.get("special", {})

HOURS = (
    config["granted"].get("PC", 0)
    + config["granted"].get("AC", 0)
    + config["granted"].get("R", 0)
)
YEAR, MONTH = config["year"], config["month"]


class MCalendar(TextCalendar):
    def __init__(self, sched=None):
        self.firstweekday = 5
        self.sched = sched or {}

    def formatday(self, day, weekday, width):
        if day == 0:
            return " ".center(width)
        else:
            return f"{day:2}".center(width)

    def formathours(self, day, weekday, width):
        if day == 0:
            return " ".center(width)
        else:
            return f"{self.sched.get(day, 0):2}".center(width)

    def formatweek(self, theweek, width):
        """
        Returns a single week in a string (no newline).
        """
        return "\n".join(
            [
                " ".join(self.formatday(d, wd, width) for (d, wd) in theweek),
                " ".join(self.formathours(d, wd, width) for (d, wd) in theweek),
            ]
        )


CALENDAR = MCalendar()
days = [d for d in CALENDAR.itermonthdates(YEAR, MONTH) if d.month == 11]


def all_assigned(assignments, variables):
    return [assignments.get(v, Unassigned) for v in variables].count(Unassigned) == 0


problem = Problem()

problem.addVariables(days, list(range(0, 17)))

for d in days:
    if d.day in special:
        problem.addConstraint(InSetConstraint([special[d.day]]), [d])
    elif d.weekday() in regular:
        problem.addConstraint(InSetConstraint([regular[d.weekday()]]), [d])

problem.addConstraint(MaxSumConstraint(HOURS))

soln = problem.getSolution()
CALENDAR.sched = {k.day: v for k, v in soln.items()}
CALENDAR.prmonth(YEAR, MONTH)

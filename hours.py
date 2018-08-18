import argparse
import decimal
import yaml
import random
import itertools

days = list(range(7))
min_hours = decimal.Decimal(13)
max_hours = decimal.Decimal(14.75)

class Task(object):

    def __init__(self, name, category, hours):
        self.name = name
        self.category = category
        self.hours = decimal.Decimal(hours)

    def with_hours(self, hours):
        """
        creates a new task like this one, but with the given hours
        """
        return Task(self.name, self.category, hours)

    def __str__(self):
        return f"{self.category}>{self.name}>{self.hours} hours"

    def __repr__(self):
        return str(self)


def get_tasks():
    with open("hours.yaml") as fp:
        c = yaml.safe_load(fp)
        return {
            task: Task(task, category, hours)
            for (category, tasks) in c.items()
            for (task, hours) in tasks.items()
        }


def day(s):
    d = int(s)
    if d < 2 or d > 7:
        raise ValueError("day must be between 2 and 7")
    return d

tasks = get_tasks()

def task(s):
    if "=" not in s:
        raise ValueError(f"format is task=# of days")

    task, days = s.split("=", 1)
    days = day(days)

    if task not in tasks:
        raise ValueError(f"task must be one of {tasks}")

    return task, days


def spread(task, days, num_days):
    if days > num_days:
        raise ValueError(f"You asked me to schedule {task} {days} days, but the client only asked for {num_days} days")

    task = tasks[task]

    if days == num_days:
        return [task] * num_days
    else:
        base = [task] * days
        for times in range(num_days - days):
            base.append(None)
        random.shuffle(base)
        return base


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--days", type=day)
    parser.add_argument("tasks", nargs="+", type=task)
    args = parser.parse_args()

    if not args.days:
        num_days = day(input("How many days does the client want service? "))
    else:
        num_days = args.days

    shuffled = [spread(tsk, days, num_days) for tsk, days in args.tasks]
    final = list(itertools.zip_longest(*shuffled))
    daily_totals = [sum([t.hours for t in tsks if t]) for tsks in final]
    for idx, tasks_ in enumerate(final):
        print(f"Daily Totals for {idx}: {daily_totals[idx]}")
        print("\n".join(["\t" + str(t) for t in tasks_ if t]))
    print(f"Weekly Hours: {sum(daily_totals)}")


if __name__ == "__main__":
    main()

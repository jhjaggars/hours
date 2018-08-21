import re

PAT = re.compile(r"(su|m|tu|w|th|f|sa)", re.I)

days = {
    "su": 0,
    "m": 1,
    "tu": 2,
    "w": 3,
    "th": 4,
    "f": 5,
    "sa": 6,
}


def match_string(s):
    for match in PAT.findall(s):
        yield days.get(match.lower())


def days_parser(s):
    if "-" in s:
        matches = list(match_string(s))
        return list(range(min(matches), max(matches) + 1))
    else:
        return list(match_string(s))

from typing import List
from collections import defaultdict
import math as m


def load(f) -> List[int]:
    o = open(f)

    line = o.readline().strip()
    nums = line.split(",")
    return [int(n) for n in nums]


def a(f):
    crabs = load(f)
    print(crabs)
    s = sorted(crabs)
    med = s[len(s) // 2]
    print(f"med {med}")
    fuel = 0
    for c in crabs:
        fuel += abs(c - med)
    print(f"fuel {fuel}")


def b(f):
    crabs = load(f)
    print(crabs)
    s = sorted(crabs)
    print(s)

    measures = {}

    def measure(m):
        if m in measures:
            return measures[m]
        fuel = 0
        for c in s:
            n = abs(m - c)
            fuel += (n * (n + 1)) // 2
        measures[m] = fuel
        return fuel

    m = (s[0] + s[-1]) // 2
    step_size = (s[-1] - s[0]) // 2

    # curve pointing down, looking for where dy/dx is positive for +/-1

    while step_size > 0:
        mv = measure(m)
        mpv = measure(m - 1)
        mnv = measure(m + 1)
        step_size = max(step_size // 2, 1)
        if mv - mpv > 0:
            print(f"at {m} values are {mpv} / {mv} / {mnv}")
            # move left
            m = m - step_size
        elif mv - mnv > 0:
            print(f"at {m} values are {mpv} \ {mv} \ {mnv}")
            # move right
            m = m + step_size
        else:
            print(f"at {m} values are {mpv} \ {mv} / {mnv}")
            # if both greater than zero we're at a local max which shouldn't be possible,
            # ditto for equal zero, so must be both less which means local min
            break

    # brute force confirm it is smooth, and actually runs fast enough for part B anyway.
    # fuels = []
    # for i in range(s[-1] + 1):
    #     fuels.append(measure(i))
    # print(fuels)
    # print(min(fuels))


# a("day7t.txt")
# a("day7.txt")

# b("day7t.txt")
b("day7.txt")

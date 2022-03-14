from collections import defaultdict


def a():
    o = open("day2.txt")
    sums = defaultdict(int)
    for line in o.readlines():
        if line:
            parts = line.split(" ")
            d, v = parts[0], int(parts[1])
            sums[d] += v
    print(sums)
    depth = sums["down"] - sums["up"]
    distance = sums["forward"]
    print(depth, distance, depth * distance)


# a()


def b():
    o = open("day2.txt")
    depth = 0
    distance = 0
    aim = 0
    for line in o.readlines():
        if line:
            parts = line.split(" ")
            d, v = parts[0], int(parts[1])
            if d == "down":
                aim += v
            elif d == "up":
                aim -= v
            elif d == "forward":
                distance += v
                depth += aim * v
    print(distance, depth, distance * depth)


b()

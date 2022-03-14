#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....

#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg

from typing import List, Tuple


def load(f) -> List[Tuple[List[str], List[str]]]:
    o = open(f)
    data = []

    for line in o.readlines():
        nums = line.strip().split(" ")
        digits, value = [], []
        seen_pipe = False
        for num in nums:
            if num == "|":
                seen_pipe = True
                continue
            num = "".join(sorted(num))
            if not seen_pipe:
                digits.append(num)
            else:
                value.append(num)
        data.append((digits, value))
    return data


# print(load("day8t.txt"))

simple_truths = {1: "cf", 4: "bcdf", 7: "acf", 8: "abcdefg"}

truths = simple_truths.copy()
truths.update(
    {2: "acdeg", 3: "acdfg", 5: "abdfg", 6: "abdefg", 9: "abcdfg", 0: "abcefg"}
)

guide = {v: k for k, v in truths.items()}

lengths = {len(v): k for k, v in simple_truths.items()}


def solve1(digits, value):
    m = {}
    for d in digits:
        if len(d) in lengths:
            m[d] = lengths[len(d)]

    # print(digits, value)
    # print(m)
    found = 0
    for v in value:
        if v in m:
            found += 1
    return found, m


# digit: segments
# 1: 2
# 7: 3
# 4: 4
# 8: 7
# 0: 6
# 6: 6
# 9: 6
# 2: 5
# 3: 5
# 5: 5

#  AAAA
# B    C
# B    C
#  DDDD
# E    F
# E    F
#  GGGG


def solveB(digits, value):
    possible = {c: set("abcdefg") for c in "ABCDEFG"}  # wires to segments
    _, m = solve1(digits, value)
    # print(m)
    for segments, v in m.items():
        for loc in simple_truths[v].upper():
            possible[loc].intersection_update(set(segments))

    # 1 = CF, the only 2 wires to 2 segments, must use both, so those wires can't be elsewhere
    for p in "ABDEG":
        possible[p].difference_update(possible["C"])
        possible[p].difference_update(possible["F"])
    # 7 = ACF so A is unique
    if len(possible["A"]) > 1:
        raise Exception(f"I'm wrong about 7 in {digits}")
    for p in "BDEG":
        possible[p].difference_update(possible["A"])
    # 4 = BDCF, and CF is 1, so BD are 2 wires to 2 segments now so must use both there
    if len(possible["B"]) > 2 or len(possible["D"]) > 2:
        raise Exception(f"I'm wrong about 4 in {digits}")
    for p in "EG":
        possible[p].difference_update(possible["B"])
        possible[p].difference_update(possible["D"])
    # 6, 9, 0 all include segment G and have 6 segments,
    # the 5 that aren't G are claimed by 1,4,7 so remaining must be G
    # they also all include F (missing C/D/E)
    for d in [d for d in digits if len(d) == 6]:
        possible["G"].intersection_update(d)
        possible["F"].intersection_update(d)
    if len(possible["G"]) > 1 or len(possible["F"]) > 1:
        raise Exception("I'm wrong about G and F in {digits}")
    for p in "BCDE":
        possible[p].difference_update(possible["G"])
        possible[p].difference_update(possible["F"])
    # 2, 3, 5 all include segment D and have 5 segments
    for d in [d for d in digits if len(d) == 5]:
        possible["D"].intersection_update(d)
    if len(possible["D"]) > 1:
        raise Exception(f"I'm wrong about D in {digits}")
    for p in "B":
        possible[p].difference_update(possible["D"])
    for p in possible:
        if len(possible[p]) > 1:
            raise Exception(f"I'm not done for {digits}")

    # print(possible)
    untangler = {v.pop(): k.lower() for k, v in possible.items()}
    digits = ""
    for v in value:
        real = "".join(sorted([untangler[s] for s in v]))
        digits += str(guide[real])
    return int(digits)


def a(f):
    data = load(f)
    total_found = 0
    for line in data:
        print()
        total_found += solve1(*line)[0]
    print(total_found)


def b(f):
    data = load(f)
    total = 0
    for line in data:
        # print()
        total += solveB(*line)
    print(total)


b("day8.txt")

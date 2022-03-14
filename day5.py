import re
from collections import defaultdict
from typing import Tuple, Dict


def load(f) -> Dict[Tuple[int, int], int]:
    o = open(f)

    w, h = 0, 0
    vents = defaultdict(int)

    for line in o.readlines():
        line = line.strip()
        m = re.match("(\d+),(\d+) -> (\d+),(\d+)", line)
        if m:
            x1, y1, x2, y2 = [int(m.group(i)) for i in [1, 2, 3, 4]]
            dx = 1 if x1 < x2 else -1
            dy = 1 if y1 < y2 else -1
            w = max(w, x1, x2)
            h = max(h, y1, y2)
            if x1 == x2 or y1 == y2:
                # axis aligned
                for x in range(x1, x2 + dx, dx):
                    for y in range(y1, y2 + dy, dy):
                        vents[(x, y)] += 1
            else:
                # diagonal
                for (x, y) in zip(range(x1, x2 + dx, dx), range(y1, y2 + dy, dy)):
                    vents[(x, y)] += 1
    return vents, w, h


def a(f):
    vents, w, h = load(f)
    if h < 11:
        for y in range(h + 1):
            line = ""
            for x in range(w + 1):
                line += str(vents[(x, y)]) if vents[(x, y)] > 0 else "."
            print(line)

    print(len([c for c in vents.values() if c >= 2]))


a("day5t.txt")
a("day5.txt")

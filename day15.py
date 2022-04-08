from collections import deque, namedtuple
from heapq import heappop, heappush
from typing import Dict, List, Set, Tuple
from adventutils import load

Point = namedtuple("Point", ["x", "y"])


def a_star(m, start=Point(0, 0), end=None):
    """thanks wikipedia"""
    width = len(m[0])
    height = len(m)
    if not end:
        end = Point(width - 1, height - 1)
    print(start, "->", end)

    def neighbors(p: Point) -> List[Point]:
        x, y = p.x, p.y
        ns = []
        if x > 0:
            ns.append(Point(x - 1, y))
        if x < width - 1:
            ns.append(Point(x + 1, y))
        if y > 0:
            ns.append(Point(x, y - 1))
        if y < height - 1:
            ns.append(Point(x, y + 1))
        return ns

    def h(p: Point):
        return end.x - p.x + end.y - p.y

    g_score: Dict[Point, int] = {}
    g_score[start] = 0  # already there

    f_score_start = g_score[start] + h(start)

    open_set: Set[Tuple[int, int]] = {start}
    open_heap: List[int, Point] = [(f_score_start, start)]

    came_from: Dict[Tuple, Tuple] = {}

    def path(p):
        c = p
        points = deque([c])
        while c != start:
            prev = came_from[c]
            points.insert(0, prev)
            c = prev
        return points

    while open_heap:
        _, current = heappop(open_heap)
        open_set.remove(current)
        if current == end:
            return g_score[end], path(end)
        for n in neighbors(current):
            maybe_gs = g_score[current] + m[n.y][n.x]
            if n not in g_score or maybe_gs < g_score[n]:
                g_score[n] = maybe_gs
                f_score_n = maybe_gs + h(n)
                came_from[n] = current
                if n not in open_set:
                    heappush(open_heap, (f_score_n, n))
                    open_set.add(n)


def _load(f):
    d = load(f)
    # convert to ints
    return [[int(i) for i in r] for r in d]


d = _load("day15.txt")

# part2, 5x the map, incrementing it
m = d
width = len(m[0])
height = len(m)
for y in range(5):
    for x in range(5):
        for _y in range(height):
            if x == 0 and y > 0:
                # create a new row
                r = []
                m.append(r)
            else:
                # re-use row we already started
                r = m[y * height + _y]
            for _x in range(width):
                if x == 0:
                    if y == 0:
                        # nothing to append, in initial square
                        continue
                    else:  # read first tile in row from above
                        risk = m[(y - 1) * height + _y][_x] + 1
                        risk = risk if risk < 10 else 1
                        r.append(risk)
                else:  # read from left
                    risk = m[y * height + _y][(x - 1) * width + _x] + 1
                    risk = risk if risk < 10 else 1
                    r.append(risk)

for r in m:
    print(".".join(map(str, r)))

score, route = a_star(m)
print(score)
# print(route)

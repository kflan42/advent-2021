from typing import Dict, List, Tuple


class CaveMap:
    def __init__(self, heightmap):
        super().__init__()
        self.heightmap = heightmap

    def risk_level(self, x, y):
        return 1 + self.heightmap[y][x]

    def is_low_point(self, x, y):
        h = self.heightmap[y][x]
        if x > 0 and h >= self.heightmap[y][x - 1]:
            return False
        if x < len(self.heightmap[0]) - 1 and h >= self.heightmap[y][x + 1]:
            return False
        if y > 0 and h >= self.heightmap[y - 1][x]:
            return False
        if y < len(self.heightmap) - 1 and h >= self.heightmap[y + 1][x]:
            return False
        return True

    def find_basins(self):
        dividing_height = 9
        basins = []  # list of sets
        points_to_basins = {}  # tuple to set
        for y in range(len(self.heightmap)):
            for x in range(len(self.heightmap[y])):
                h = self.heightmap[y][x]
                # each point each divides
                if h == dividing_height:
                    continue
                sx, sy = None, None
                # or adds to or joins basins
                if x > 0 and (x - 1, y) in points_to_basins:
                    sx = points_to_basins[(x - 1, y)]
                if y > 0 and (x, y - 1) in points_to_basins:
                    sy = points_to_basins[(x, y - 1)]
                # or starts one
                if not (sx or sy):
                    s = set()
                    basins.append(s)
                elif sx and sy and sx != sy:
                    # join them, have sx win
                    basins.remove(sy)
                    sx.update(sy)
                    for p in sy:
                        points_to_basins[p] = sx
                    s = sx
                elif sx:
                    s = sx
                elif sy:
                    s = sy
                else:
                    raise Exception("uh oh")
                s.add((x, y))
                points_to_basins[(x, y)] = s
        return basins


def load(f) -> CaveMap:  # List[List[int]]:
    o = open(f)

    heightmap = []

    for line in o.readlines():
        line = line.strip()
        if not line:
            continue
        row = []
        for h in line:
            row.append(int(h))
        heightmap.append(row)

    return CaveMap(heightmap)


def a(f):
    cave = load(f)
    risk = 0
    for y in range(len(cave.heightmap)):
        for x in range(len(cave.heightmap[y])):
            if cave.is_low_point(x, y):
                risk += cave.risk_level(x, y)
    print(risk)


def b(f):
    cave = load(f)
    basins = sorted(cave.find_basins(), key=lambda b: -len(b))
    a, b, c = basins[0:3]
    print(len(a) * len(b) * len(c))


b("day9.txt")

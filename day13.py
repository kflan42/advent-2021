import re
from adventutils import load

# fold up for y= lines
# fold left for x= lines
# so higher values map onto lower ones

# d = load("day13t.txt")
d = load("day13.txt")

def _load(d):
    dots = []
    folds = []
    for line in d:
        if re.match(r"\d+,\d+", line):
            x,y = [int(i) for i in line.split(",")]
            dots.append((x,y))
            continue
        m = re.match(r"fold along (\w)=(\d+)", line)
        if m:
            axis = m.group(1)
            value = int(m.group(2))
            folds.append((axis, value))
    return dots,folds

dots, folds = _load(d)

# print(dots, folds)

visible_dots = set(dots)

def fold(axis, value, visible_dots):
    ai = 0 if axis == 'x' else 1  # offset into dot tuple
    oi = 1 if axis == 'x' else 0
    resulting = set()
    for d in visible_dots:
        if d[ai] > value:
            d_f = (2*value - d[ai], d[oi]) if axis == 'x' else (d[oi], 2*value - d[ai])
            resulting.add(d_f)
        else:
            resulting.add(d)
    return resulting

def render(visible_dots):
    mx = max([vd[0] for vd in visible_dots])
    my = max([vd[1] for vd in visible_dots])
    for y in range(my+1):
        line = [ '#' if (x,y) in visible_dots else '.' for x in range(mx+1) ]
        print("".join(line))
    print()

for f in folds:
    visible_dots = fold(f[0], f[1], visible_dots)
render(visible_dots)
# visible_dots = fold(folds[0][0], folds[0][1], visible_dots)
# print(len(visible_dots))
# print(visible_dots)

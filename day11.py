from typing import List, Tuple
from adventutils import load


def step(energies) -> Tuple[List[List[int]], int]:
    """
    perform a step, return new energy levels and number of flashes that occured
    """
    # plus 1 to all
    energies = [[i + 1 for i in line] for line in energies]

    flashes = [0]  # hacky pointer
    flashed = [[False for i in line] for line in energies]
    # any over 9 flash = inc adj by 1, they might flash. each flash at most 1x per step.
    def flash(x, y):
        flashed[y][x] = True
        flashes[0] += 1
        for y1 in range(max(0, y - 1), min(len(energies), y + 1 + 1)):
            for x1 in range(max(0, x - 1), min(len(energies[y]), x + 1 + 1)):
                if y1 == y and x1 == x:
                    continue # don't bump self
                e = energies[y1][x1]
                e += 1
                energies[y1][x1] = e
                if e >= 10 and not flashed[y1][x1]:
                    flash(x1, y1)

    # look at every octopus, propagate flashes via recursion
    for y in range(len(energies)):
        for x in range(len(energies[y])):
            if energies[y][x] >= 10 and not flashed[y][x]:
                flash(x, y)

    # any that flashed drop to 0
    for y in range(len(energies)):
        for x in range(len(energies[y])):
            if flashed[y][x]:
                energies[y][x] = 0

    return energies, flashes[0]


def render(energies):
    for line in energies:
        print("".join(str(i) for i in line))
    print()


def a(f):
    d = load(f)
    energies = [[int(i) for i in line] for line in d]
    render(energies)

    total_flashes = 0
    for i in range(100):
        print(f"step {i+1}")
        energies, flashes = step(energies)
        total_flashes += flashes
        if i+1 < 10 or i+1 % 10 == 0:
            render(energies)

    print(total_flashes)

def b(f):
    d = load(f)
    energies = [[int(i) for i in line] for line in d]
    size = len(energies) * len(energies[0]) # assume square
    flashed = 0
    steps = 0
    while flashed != size:
        steps += 1
        energies, flashed = step(energies)
    print(steps)

b("day11.txt")

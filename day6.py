from typing import List
from collections import defaultdict


def load(f) -> List[int]:
    o = open(f)

    line = o.readline().strip()
    nums = line.split(",")
    fish = [int(n) for n in nums]
    return fish


def a(f, duration):
    fish = load(f)
    print(fish)

    for d in range(1, duration + 1):
        new_fish = []
        births = 0
        for f in fish:
            nf = f - 1
            if nf == -1:
                new_fish.append(6)  # reset
                births += 1
            else:
                new_fish.append(nf)

        fish = new_fish + [8] * births
        if (
            d == 80
        ):  # part 2 is 256. This naive solution runs out of cpu time and maybe eventually ram.
            print(f"Day {d}, Count {len(fish)}: ")  # + str(fish))
    return len(fish)


def b(f, duration):
    fish = load(f)
    print(fish)

    fish_days = defaultdict(int)
    for f in fish:
        fish_days[f] += 1

    for day in range(1, duration + 1):
        new_fd = defaultdict(int)
        for d, f in fish_days.items():
            d = d - 1
            if d == -1:
                new_fd[8] += f
                new_fd[6] += f
            else:
                new_fd[d] += f
        fish_days = new_fd
        if (
            day == 18 or day == 80 or day == 256
        ):  # part 2 is 256. This naive solution runs out of cpu time and maybe eventually ram.
            print(f"Day {day}, Count {sum(fish_days.values())}: ")  # + str(fish))
    return sum(fish_days.values())


print(b("day6.txt", 256))

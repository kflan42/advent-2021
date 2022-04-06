from collections import Counter, defaultdict
from datetime import datetime
from itertools import chain
from typing import Dict, List
from adventutils import load


def init(f):
    d = load(f)
    pt = [c for c in d[0]]
    rules = d[2:]
    rule_map = {}
    for r in rules:
        pair = r[0:2]
        ins = r[-1]
        rule_map[(pair[0], pair[1])] = ins
    return pt, rule_map


def step(polymer, rule_map):
    pairs = zip(polymer[:-1], polymer[1:])
    r = chain.from_iterable([p[0], rule_map[p]] for p in pairs)
    r1 = list(r)
    r1.append(polymer[-1])
    return r1


def convert(polymer: List[str]) -> Dict:
    return Counter(zip(polymer[:-1], polymer[1:]))


def step_b(polymer, rule_map):
    new_pairs = defaultdict(int)
    for p, cnt in polymer.items():
        np1 = (p[0], rule_map[p])
        np2 = (rule_map[p], p[1])
        new_pairs[np1] += cnt
        new_pairs[np2] += cnt
    return new_pairs


polymer, rule_map = init("day14.txt")
polymer_b = convert(polymer)
print(polymer, polymer_b)

start = datetime.now()

steps = 40  # 10 for part a

for i in range(steps):
    if i < 10:
        polymer = step(polymer, rule_map)
    polymer_b = step_b(polymer_b, rule_map)
    # print(polymer, polymer2)
    elapsed = datetime.now() - start
    print(
        "step", i + 1, "elapsed", elapsed.total_seconds(), sum(polymer_b.values()) + 1
    )

print("done")

if steps <= 10:
    print("part a lengths", len(polymer), sum(polymer_b.values()) + 1)
    c = Counter(polymer)
    counts = c.most_common()
    print("part a answer", counts[0][1] - counts[-1][1])

firsts = defaultdict(int)
# last char never changed from the input
last_char = polymer[-1]
for p, cnt in polymer_b.items():
    firsts[p[0]] += cnt
firsts[last_char] += 1

maximum = last_char, firsts[last_char]
minimum = last_char, firsts[last_char]
for f, cnt in firsts.items():
    if cnt > maximum[1]:
        maximum = f, cnt
    if cnt < minimum[1]:
        minimum = f, cnt
print("part b answer", maximum[1] - minimum[1])

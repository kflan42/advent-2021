from collections import namedtuple
import copy
from dataclasses import dataclass, field
import re
from typing import Dict, List, Set
from typing_extensions import Self
from adventutils import load

def _load(f):
    maps = []
    Map = namedtuple("Map", ["edges", "count", "paths"])
    m = None
    for line in load(f):
        if not m and line:
            m = Map([], 0, [])
        if '-' in line:
            m.edges.append(line)
        elif ',' in line:
            m.paths.append(line)
        elif re.match(r'\d+', line):
            m = Map(m.edges, int(line), m.paths)
        elif m and not line:
            maps.append(m)
            m = None
    if m:
        maps.append(m)
    return maps


@dataclass
class Node:
    """One could just use a Dict[str,Set[str]] instead."""
    name: str
    edges: List[Self] = field(default_factory=list)


def _transform(map) -> Dict[str, Node]:
    nodes = dict()
    for e in map.edges:
        n1, n2 = e.split('-')
        node1 = nodes.setdefault(n1,  Node(name=n1))
        node2 = nodes.setdefault(n2,  Node(name=n2))
        node1.edges.append(node2)
        node2.edges.append(node1)
    return nodes

# Typical DFS is O(|V|+|E|), though the cyclic nature and special rules recessitate some extra bookkeeping.
# Here I used recursion so the stack is the python call stack.
# This adds a *E term since the "been" list is constructed each time rather than built and passed along.
# This also adds a *E term for part_b due to checking a list if we've visited a lower case cave twice yet.

def _traverse(start: Node, path:List[Node], part_b=False) -> List[List[Node]]:
    """return all paths from this node"""
    # edges are bidirectional
    # can only visit lowercase nodes once
    # valid paths go start-.*-end
    path = copy.copy(path)
    path.append(start)
    paths = []
    been = [p.name for p in path if p.name == p.name.lower()]
    if not part_b:
        been = set(been) # optimization
    for n in start.edges:
        if n.name == n.name.lower() and n.name in been:
            if part_b and n.name not in ["start", "end"] and len(been) == len(set(been)):
                # no repeat yet, so this one can
                paths.extend(_traverse(n, path, part_b=part_b))
            else:
                continue # can't revist lowercase node
        elif n.name == "end":
            # base/termination case
            full_path = copy.copy(path)
            full_path.append(n)
            paths.append(full_path)
        else:
            paths.extend(_traverse(n, path, part_b=part_b))
    return paths



def x(f, i, part_b=False):
    d = _load(f)
    graph = _transform(d[i])
    for k,v in graph.items():
        print(v.name, "--", [e.name for e in v.edges])
    paths = _traverse(graph['start'], [], part_b=part_b)
    print(len(paths))
    if len(paths) < 20:
        for p in paths:
            print(",".join([n.name for n in p]))
    print()

x("day12t.txt", 0)
x("day12t.txt", 1)
x("day12t.txt", 2)
x("day12.txt", 0)

print("----")

x("day12t.txt", 0, True)
x("day12t.txt", 1, True)
x("day12t.txt", 2, True)
x("day12.txt", 0, True)


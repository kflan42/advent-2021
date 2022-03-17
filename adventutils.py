from typing import List


def load(f) -> List[str]:
    with open(f) as o:
        return [l.strip() for l in o.readlines()]
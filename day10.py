from typing import List


delims = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}
points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
points2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
} 

def load(f) -> List[str]:
    with open(f) as o:
        return [l.strip() for l in o.readlines()]

def ab(f):
    score1 = 0
    scores = []
    for li in load(f):
        stack = []
        corrupt = False
        for c in li:
            if c in delims:
                stack.append(c)
            else:
                need = delims[stack[-1]]
                if c == need:
                    stack.pop()
                else:
                    # corrupt
                    score1 += points[c]
                    corrupt = True
                    break
        if not corrupt and stack:
            # incomplete
            score = 0
            while stack:
                need = delims[stack.pop()]
                score *= 5
                score += points2[need]
            scores.append(score)
    scores.sort()
    score2 = scores[len(scores)//2]
    return score1, score2

print(ab("day10.txt"))
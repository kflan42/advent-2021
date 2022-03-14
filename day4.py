class Board:

    # n112umbers:List[List[int]] = []
    # marked:List[List[bool]] = []

    def __init__(self, nums):
        super().__init__()
        self.numbers = nums
        size = len(nums)
        self.marked = [[False] * size for s in range(size)]

    def score(self, winner) -> int:
        unmarked = 0
        for r, row in enumerate(self.numbers):
            for c, val in enumerate(row):
                if not self.marked[r][c]:
                    unmarked += val
        return unmarked * winner

    def mark(self, number) -> bool:
        for r, row in enumerate(self.numbers):
            for c, val in enumerate(row):
                if val == number:
                    self.marked[r][c] = True
                    if all(self.marked[r]):
                        return True
                    if all([m[c] for m in self.marked]):
                        return True
        return False

    def __repr__(self):
        return f"{self.numbers}\n{self.marked}\n"


def load():
    o = open("day4.txt")

    first = o.readline().strip()
    calls = [int(w) for w in first.split(",") if w]

    boards: List[Board] = []
    numbers = []
    i = 0
    for line in o.readlines():
        line = line.strip()
        if line:
            i += 1
            numbers.append([int(w) for w in line.split(" ") if w])
            if i == 5:
                boards.append(Board(numbers))
                numbers = []
                i = 0
    return calls, boards


def a():
    calls, boards = load()
    # print(boards)

    for call in calls:
        for board in boards:
            if board.mark(call):
                print("winner")
                print(board)
                print(board.score(call))
                exit(0)


def b():
    calls, boards = load()
    winners = set()
    for call in calls:
        for board in boards:
            if board.mark(call):
                winners.add(board)
                if len(winners) == len(boards):
                    print("last winner")
                    print(board)
                    print(board.score(call))
                    exit(0)


b()

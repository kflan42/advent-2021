o = open("day1.txt")
prev = None
incs = 0
prev = int(o.readline())
for line in o.readlines():
    if line:
        val = int(line)
        if val > prev:
            incs += 1
        prev = val

print(incs)

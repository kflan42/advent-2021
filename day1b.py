o = open("day1.txt")
prev = None
incs = 0
a, b, c = int(o.readline()), int(o.readline()), int(o.readline())
for line in o.readlines():
    if line:
        val = int(line)
        if val + c + b > a + b + c:
            incs += 1
        a = b
        b = c
        c = val

print(incs)

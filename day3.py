def a():
    o = open("day3.txt")
    bits = []
    for line in o.readlines():
        if line:
            line = line.strip()
            if not bits:
                bits = [0] * len(line)
            for i, c in enumerate(line):
                bits[i] += int(c) * 2 - 1
    print(bits)
    gamma = "".join("1" if b > 0 else "0" for b in bits)
    epsilon = "".join("1" if b < 0 else "0" for b in bits)
    g = int(gamma, 2)
    e = int(epsilon, 2)
    print(gamma, g)
    print(epsilon, e)
    print(g * e)


# a()


def b():
    o = open("day3.txt")
    bits = []
    length = 0
    for line in o.readlines():
        if line:
            line = line.strip()
            if not length:
                length = len(line)  # all same
            bits.append(int(line, 2))

    def most_common(bits, shifter):
        v = 0

        for b in bits:
            if b >> shifter & 0b1:
                v += 1
            else:
                v -= 1
        return 1 if v >= 0 else 0

    def determine(bits, flip):
        filtered = bits
        for i in range(length):
            shifter = length - i - 1
            mc_c = most_common(filtered, shifter)
            if flip:
                mc_c = mc_c ^ 1
            filtered = [b for b in filtered if (b >> shifter & 0b1) == mc_c]
            if len(filtered) == 1:
                return filtered[0]

    oxygen = determine(bits, False)
    co2 = determine(bits, True)

    print(oxygen, co2, oxygen * co2)


b()

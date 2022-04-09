from cmath import inf
from dataclasses import dataclass
from functools import reduce
from itertools import product
from typing import Any, List, Optional, Tuple
from adventutils import load

hex_bits = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


@dataclass
class Packet:
    v: int
    t: int
    literal: Optional[int]
    subs: List[Any]


def decode(bits, i=0) -> Tuple[int, Packet]:
    v = int(bits[i : i + 3], 2)
    t = int(bits[i + 3 : i + 6], 2)
    i += 6
    if t == 4:  # literal
        number = ""
        while i < len(bits):
            chunk = bits[i : i + 5]
            i += 5
            number += chunk[1:]
            if chunk[0] == "0":
                break
        return i, Packet(v=v, t=t, literal=int(number, 2), subs=[])
    else:  # operator
        length_type_id = bits[i]
        i += 1
        total_length_in_bits, sub_packet_count = inf, inf
        if length_type_id == "0":
            total_length_in_bits = int(bits[i : i + 15], 2)
            i += 15
        else:
            sub_packet_count = int(bits[i : i + 11], 2)
            i += 11
        i_start = i
        subs = []
        while i - i_start < total_length_in_bits and len(subs) < sub_packet_count:
            i, p = decode(bits, i)
            subs.append(p)
        return i, Packet(v=v, t=t, literal=None, subs=subs)


def part1(packet: Packet) -> int:
    version_sum = 0
    stack = [packet]
    while stack:
        current = stack.pop()
        version_sum += current.v
        stack.extend(current.subs)
    return version_sum


def part2(packet: Packet) -> int:
    def eval_pkt(packet: Packet) -> int:
        if packet.t == 4:
            return packet.literal
        elif packet.t == 0:
            return sum([eval_pkt(p) for p in packet.subs])
        elif packet.t == 1:
            return reduce(lambda x, y: x * y, [eval_pkt(p) for p in packet.subs])
        elif packet.t == 2:
            return min([eval_pkt(p) for p in packet.subs])
        elif packet.t == 3:
            return max([eval_pkt(p) for p in packet.subs])
        elif packet.t == 5:
            return 1 if eval_pkt(packet.subs[0]) > eval_pkt(packet.subs[1]) else 0
        elif packet.t == 6:
            return 1 if eval_pkt(packet.subs[0]) < eval_pkt(packet.subs[1]) else 0
        elif packet.t == 7:
            return 1 if eval_pkt(packet.subs[0]) == eval_pkt(packet.subs[1]) else 0

    return eval_pkt(packet)


d = load("day16.txt")
for line in d:
    bits = "".join([hex_bits[x] for x in line])
    # print(bits)
    _, packet = decode(bits)
    # print(packet)
    print("part1", part1(packet), "part2", part2(packet))

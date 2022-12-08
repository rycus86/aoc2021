from shared.utils import *

from functools import cmp_to_key


class Pair(object):
    left: List
    right: List

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def has_right_order(self):
        return self.root_compare() < 0

    def root_compare(self):
        return self.compare(self.left, self.right)

    def compare(self, left, right):
        if isinstance(left, list):
            if isinstance(right, list):
                for idx in range(min(len(left), len(right))):
                    cmp = self.compare(left[idx], right[idx])
                    if cmp != 0:
                        return cmp
                else:
                    if len(left) < len(right):
                        return -1
                    elif len(left) > len(right):
                        return 1
            elif isinstance(right, int):
                return self.compare(left, [right])
        elif isinstance(left, int):
            if isinstance(right, list):
                return self.compare([left], right)
            elif isinstance(right, int):
                if left < right:
                    return -1
                elif left > right:
                    return 1
                elif left == right:
                    return 0

        return 0


class Day13(Solution):
    packets: List
    pairs: List[Pair]

    def setup(self):
        self.packets = list()
        self.pairs = list()

        prev = None

        for line in self.input_lines():
            if line.startswith('['):
                item = eval(line)
                self.packets.append(item)

                if prev is not None:
                    self.pairs.append(Pair(prev, item))
                    prev = None
                else:
                    prev = item

    def part_1(self):
        for idx, pair in enumerate(self.pairs):
            if pair.has_right_order():
                self.add_result(idx + 1)

    def part_2(self):
        key_2, key_6 = [[2]], [[6]]

        self.packets.append(key_2)
        self.packets.append(key_6)

        def compare_packets(x, y):
            return Pair(x, y).root_compare()

        ordered = list(sorted(self.packets, key=cmp_to_key(compare_packets)))

        idx_2, idx_6 = ordered.index(key_2), ordered.index(key_6)

        return (idx_2 + 1) * (idx_6 + 1)


Day13(__file__).solve()

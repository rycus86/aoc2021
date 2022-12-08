from shared.utils import *


class Rucksack(object):
    def __init__(self, items):
        self.left = set(self._convert(x) for x in items[0:len(items) // 2])
        self.right = set(self._convert(x) for x in items[len(items) // 2:])

    @staticmethod
    def _convert(letter):
        if 'a' <= letter <= 'z':
            return ord(letter) - ord('a') + 1
        else:
            return ord(letter) - ord('A') + 27

    def common(self):
        return next(iter(self.left.intersection(self.right)))

    def all_items(self):
        return self.left.union(self.right)

    def find_badge(self, x, y):
        return next(iter(
            self.all_items()
                .intersection(x.all_items())
                .intersection(y.all_items())))


class Day03(Solution):
    rucksacks: List[Rucksack]

    def setup(self):
        self.rucksacks = [Rucksack(line) for line in self.input_lines()]

    def part_1(self):
        return sum(r.common() for r in self.rucksacks)

    def part_2(self):
        idx = 0
        while idx < len(self.rucksacks):
            a, b, c = self.rucksacks[idx:idx+3]  # type: Rucksack
            idx += 3

            self.add_result(a.find_badge(b, c))


Day03(__file__).solve()

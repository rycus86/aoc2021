from shared.utils import *


class Pair(object):

    def __init__(self, line):
        left, right = line.split(',')
        self.left = tuple(map(int, left.split('-')))
        self.right = tuple(map(int, right.split('-')))

    def fully_contains_one(self):
        a, b = self.left, self.right
        if self._length(a) < self._length(b):
            a, b = b, a

        return a[0] <= b[0] and a[1] >= b[1]

    def overlaps(self):
        a, b = self.left, self.right
        if a[0] > b[0]:
            a, b = b, a

        return a[0] <= b[0] <= a[1] or b[0] <= a[1] <= b[1]

    @staticmethod
    def _length(items):
        return len(range(items[0], items[1] + 1))


class Day04(Solution):
    pairs: List[Pair]

    def setup(self):
        self.pairs = [Pair(line) for line in self.input_lines()]

    def part_1(self):
        return sum(1 for p in self.pairs if p.fully_contains_one())

    def part_2(self):
        return sum(1 for p in self.pairs if p.overlaps())


Day04(__file__).solve()

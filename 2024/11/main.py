from shared.utils import *
from functools import cache


class Day11(Solution):
    stones: list[int]

    def setup(self):
        self.stones = list(map(int, self.input.split()))

    def part_1(self):
        return sum(self._split_stones(s, 25) for s in self.stones)

    def part_2(self):
        return sum(self._split_stones(s, 75) for s in self.stones)

    @cache
    def _split_stones(self, value: int, remaining: int):
        if remaining == 0:
            return 1

        if value == 0:
            return self._split_stones(1, remaining - 1)
        elif len(str(value)) % 2 == 0:
            s, l = str(value), len(str(value)) // 2
            a, b = map(int, (s[0:l], s[l:]))
            return self._split_stones(a, remaining - 1) + self._split_stones(b, remaining - 1)
        else:
            return self._split_stones(value * 2024, remaining - 1)


Day11(__file__).solve()

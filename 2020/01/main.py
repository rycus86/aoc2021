from shared.utils import *


class Day01(Solution):
    numbers: List[int]

    def setup(self):
        self.numbers = list(map(int, self.input_lines()))

    def part_1(self):
        for idx, start in enumerate(self.numbers):
            for end in self.numbers[idx + 1:]:
                if start + end == 2020:
                    return start * end

    def part_2(self):
        for i1, first in enumerate(self.numbers):
            for i2, second in enumerate(self.numbers[i1 + 1:]):
                if first + second > 2020:
                    continue

                for third in self.numbers[i2 + 1:]:
                    if first + second + third == 2020:
                        return first * second * third


Day01(__file__).solve()

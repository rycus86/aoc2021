from shared.utils import *


class Day09(Solution):
    preamble_length = 25
    numbers: List[int]

    def setup(self):
        self.numbers = list(map(int, self.input_lines()))

    def part_1(self):
        preamble = self.numbers[0:self.preamble_length]
        for value in self.numbers[self.preamble_length:]:
            if value in self.iter_pair_sums(preamble):
                preamble = preamble[1:] + [value]
            else:
                return value

    def part_2(self):
        target = self.part_1()
        for i, cmp in enumerate(self.numbers):
            for j, value in enumerate(self.numbers[i+1:]):
                cmp += value
                if cmp == target:
                    numbers = self.numbers[i:i+j+2]
                    return min(numbers) + max(numbers)
                elif cmp > target:
                    break

    def iter_pair_sums(self, values):
        for i, first in enumerate(values):
            for second in values[i+1:]:
                yield first + second


Day09(__file__).solve()

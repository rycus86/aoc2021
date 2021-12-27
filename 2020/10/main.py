from collections import Counter

from shared.utils import *


class Day10(Solution):
    adapters: List[int]
    adapters_len = int

    def setup(self):
        self.adapters = [0] + list(sorted(map(int, self.input_lines())))
        self.adapters_len = len(self.adapters)

    def part_1(self):
        differences = Counter()
        for idx, value in enumerate(self.adapters[1:]):
            diff = value - self.adapters[idx]
            differences[diff] += 1

        differences[3] += 1  # built-in adapter

        return differences[1] * differences[3]

    def part_2(self):
        choices = [1] * len(self.adapters)

        for idx, value in reversed(list(enumerate(self.adapters[:-1]))):
            choices[idx] = sum(choices[idx+i+1] for i, n in enumerate(self.adapters[idx+1:idx+4]) if 1 <= n - value <= 3)

        return choices[0]

    def _part_2(self):
        self.consume(0, [0])

    def consume(self, from_index, prev):
        start = self.adapters[from_index]
        for idx in (1, 2, 3):
            if idx == 1 and from_index == self.adapters_len - 1:
                self.add_result()
                break
            elif from_index + idx >= self.adapters_len:
                break

            value = self.adapters[from_index + idx]
            if 1 <= value - start <= 3:
                self.consume(from_index + idx, prev + [value])


Day10(__file__).solve()

from shared.utils import *

from collections import defaultdict


class Day01(Solution):
    elves: Dict[int, int]

    def setup(self):
        self.elves = defaultdict(lambda: 0)

        current = 0
        for line in self.input_lines():
            if not line.strip():
                current += 1
            else:
                self.elves[current] += int(line.strip())

    def part_1(self):
        return max(self.elves.values())

    def part_2(self):
        return sum(list(sorted(self.elves.values(), reverse=True))[0:3])


Day01(__file__).solve()

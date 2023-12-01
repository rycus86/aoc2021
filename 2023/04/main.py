import re

from shared.utils import *


class Day04(Solution):

    def part_1(self):
        for line in self.input_lines():
            common = self._get_common_numbers(line)
            if common > 0:
                self.add_result(2 ** (common - 1))

    def part_2(self):
        multipliers = defaultdict(lambda: 1)

        for idx, line in enumerate(self.input_lines()):
            common = self._get_common_numbers(line)
            for w in range(common):
                multipliers[idx + w + 1] += multipliers[idx]
            self.add_result(multipliers[idx])

    @staticmethod
    def _get_common_numbers(line: str):
        line, _ = re.subn(r'\s+', ' ', line)
        _, parts = line.strip().split(':')
        left, right = map(str.strip, parts.split('|'))
        winning = set(map(int, left.split(' ')))
        mine = set(map(int, right.split(' ')))
        return len(mine.intersection(winning))


Day04(__file__).solve()

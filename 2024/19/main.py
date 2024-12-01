from shared.utils import *
from functools import cache


class Day19(Solution):
    available: dict[str, set[str]]
    designs: list[str]

    def setup(self):
        self.designs = list()

        for line in self.input_lines():
            if ',' in line:
                self.available = defaultdict(set)
                for item in map(str.strip, line.split(',')):
                    self.available[item[0]].add(item)

            elif line.strip():
                self.designs.append(line.strip())

    @cache
    def count_arrangements(self, design):
        if not design:
            return 1

        total = 0

        for a in self.available[design[0]]:
            if design.startswith(a):
                if na := self.count_arrangements(design[len(a):]):
                    total += na

        return total

    def part_1(self):
        return sum(1 for d in self.designs if self.count_arrangements(d))

    def part_2(self):
        return sum(self.count_arrangements(d) for d in self.designs)


Day19(__file__).solve()

from shared.utils import *


class Day09(Solution):
    series: List[List[int]]

    def setup(self):
        self.series = list()
        for line in self.input_lines():
            self.series.append(list(map(int, line.split())))

    def part_1(self):
        for items in self.series:
            last_values = list()
            diff = list(items)
            while not all(d == 0 for d in diff):
                last_values.append(diff[-1])
                diff = [p - diff[i] for i, p in enumerate(diff[1:])]
            self.add_result(sum(last_values))

    def part_2(self):
        for items in self.series:
            first_values = list()
            diff = list(items)
            while not all(d == 0 for d in diff):
                first_values.append(diff[0])
                diff = [p - diff[i] for i, p in enumerate(diff[1:])]
            cmp = 0
            for fv in reversed(first_values):
                cmp = fv - cmp
            self.add_result(cmp)


Day09(__file__).solve()

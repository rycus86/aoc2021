from shared.utils import *


class Day15(Solution):
    starting: List[int]

    def setup(self):
        self.starting = list(map(int, self.input.split(',')))

    def part_1(self):
        debug = self.solve_for(2020)
        assert debug == 289
        return debug

    def part_2(self):
        debug = self.solve_for(30000000)
        assert debug == 1505722
        return debug

    def solve_for(self, target):
        memory = [-1] * target  # this list appears slightly faster than a dict
        for idx, value in enumerate(self.starting):
            memory[value] = idx

        index, value = len(self.starting), 0

        while index < target - 1:
            if memory[value] > -1:
                previous, memory[value] = memory[value], index
                value = index - previous
            else:
                memory[value] = index
                value = 0

            index += 1

        return value


Day15(__file__).solve()

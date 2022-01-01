from shared.utils import *


class Day01(Solution):

    def part_1(self):
        for value in map(int, self.input_lines()):
            self.add_result(value // 3 - 2)

    def part_2(self):
        for value in map(int, self.input_lines()):
            to_add = value // 3 - 2
            while to_add > 0:
                self.add_result(to_add)
                to_add = to_add // 3 - 2


Day01(__file__).solve()

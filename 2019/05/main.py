from shared.utils import *
from shared.intcode import IntCodeProgram


class Day05(Solution):
    program: IntCodeProgram

    def setup(self):
        self.program = IntCodeProgram(list(map(int, self.input.split(','))))

    def part_1(self):
        result = self.program.run([1])
        while result == 0:
            result = self.program.run([])
        return result

    def part_2(self):
        result = self.program.run([5])
        while result == 0:
            result = self.program.run([])
        return result


Day05(__file__).solve()

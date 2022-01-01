import itertools

from shared.utils import *
from shared.intcode import IntCodeProgram


class Day07(Solution):
    program: IntCodeProgram

    def setup(self):
        self.program = IntCodeProgram(list(map(int, self.input.split(','))))

    def part_1(self):
        self.evaluate_part1(0, 0, list())

    def evaluate_part1(self, digit: int, previous: int, already_used: List[int]):
        for x in range(5):
            if x in already_used:
                continue

            result = self.program.clone().run([x, previous])
            if result is None:
                continue
            if digit == 4:
                self.max_result(result)
            else:
                self.evaluate_part1(digit + 1, result, already_used + [x])

    def part_2(self):
        for digits in itertools.permutations([5, 6, 7, 8, 9]):
            digits = {idx: d for idx, d in enumerate(digits)}
            programs = {idx: self.program.clone() for idx in range(5)}

            next_program = 0
            previous_result = 0
            remaining_phases = 5

            while True:
                if remaining_phases > 0:
                    inputs = [digits[next_program], previous_result]
                    remaining_phases -= 1
                else:
                    inputs = [previous_result]

                result = programs[next_program].run(inputs)

                if programs[next_program].is_done():
                    self.max_result(previous_result)
                    break
                else:
                    next_program = (next_program + 1) % 5
                    previous_result = result

        assert self._counted_results == 1336480, f'{self._counted_results} != 1336480'


Day07(__file__).solve()

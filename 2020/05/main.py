from shared.utils import *


class Day05(Solution):
    def part_1(self):
        return max(map(self.calculate, self.input_lines()))

    def part_2(self):
        seats = list(sorted(map(self.calculate, self.input_lines())))
        for idx, seat in enumerate(seats[1:]):
            if seats[idx] != seat - 1:
                return seat - 1

    def calculate(self, entry):
        r1, r2, c1, c2 = 0, 127, 0, 7
        for e in entry:
            r_diff = (r2 - r1 + 1) // 2
            c_diff = (c2 - c1 + 1) // 2

            if e == 'F':
                r2 -= r_diff
            elif e == 'B':
                r1 += r_diff
            elif e == 'L':
                c2 -= c_diff
            elif e == 'R':
                c1 += c_diff

        assert r1 == r2
        assert c1 == c2

        return r1 * 8 + c1


Day05(__file__).solve()

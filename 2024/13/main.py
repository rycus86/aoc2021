from shared.utils import *
import re
import math


class Day13(Solution):
    button_a = list[tuple[int, int]]
    button_b = list[tuple[int, int]]
    prizes = list[tuple[int, int]]

    def setup(self):
        self.button_a = list()
        self.button_b = list()
        self.prizes = list()

        index = 0
        xy_pattern = re.compile(r'.+: X[=+](\d+), Y[=+](\d+)')

        for line in self.input_lines():
            if not line.strip():
                index += 1
                continue

            x, y = map(int, xy_pattern.match(line).groups())
            if line.startswith('Button A:'):
                self.button_a.append((x, y))
            elif line.startswith('Button B:'):
                self.button_b.append((x, y))
            elif line.startswith('Prize:'):
                self.prizes.append((x, y))

    def part_1(self):
        self._calculate()

    def part_2(self):
        for idx, (px, py) in enumerate(self.prizes):
            self.prizes[idx] = (px := px + 10000000000000, py := py + 10000000000000)

        self._calculate()

    def _calculate(self):
        for idx, (px, py) in enumerate(self.prizes):
            ax, ay = self.button_a[idx]
            bx, by = self.button_b[idx]

            blcm = math.lcm(bx, by)
            bm1, bm2 = blcm // bx, blcm // by

            a1, a2, p1, p2 = ax * bm1, ay * bm2, px * bm1, py * bm2
            a, p = a2 - a1, p2 - p1
            ra, rem = p // a, p % a
            if rem == 0:
                rb = (px - ra * ax) // bx
                self.add_result(ra * 3 + rb)

Day13(__file__).solve()

import re
from itertools import combinations

from shared.utils import *


class Day14(Solution):
    memory: Dict[int, int]

    def setup(self):
        self.memory = dict()

    def part_1(self):
        mask = None

        for line in self.input_lines():
            if line.startswith('mask = '):
                mask = list()
                for idx, m in enumerate(line[len('mask = '):]):
                    if m != 'X':
                        mask.append((2 ** (35 - idx), int(m)))

            elif line.startswith('mem'):
                address, target = map(int, re.match(r'mem\[([0-9]+)] = ([0-9]+)', line).groups())

                for masked, change in mask:
                    if target & masked != masked * change:
                        target ^= masked

                self.memory[address] = target

        return sum(self.memory.values())

    def part_2(self):
        mask, floating, enable = None, None, None

        for line in self.input_lines():
            if line.startswith('mask = '):
                line = line[len('mask = '):]

                mask = int(line
                           .replace('0', 'x')
                           .replace('X', '0')
                           .replace('1', '0')
                           .replace('x', '1'), 2)

                x_positions, floating = list(), [0]
                enable = 0

                for idx, m in enumerate(line):
                    if m == '1':
                        enable += 2 ** (35 - idx)
                    elif m == 'X':
                        x_positions.append(2 ** (35 - idx))

                for r in range(1, len(x_positions) + 1):
                    floating.extend(map(sum, combinations(x_positions, r)))

            elif line.startswith('mem'):
                address, target = map(int, re.match(r'mem\[([0-9]+)] = ([0-9]+)', line).groups())

                address &= mask
                address += enable

                for extra in floating:
                    self.memory[address + extra] = target

        return sum(self.memory.values())


Day14(__file__).solve()

import re

from shared.utils import *


class Day08(Solution):
    instructions: str
    map: Dict[str, Dict[str, str]]

    def setup(self):
        self.instructions = ''
        self.map = dict()

        for line in self.input_lines():
            if not self.instructions:
                self.instructions = line.strip()
                continue

            if not line.strip():
                continue

            pos, lr = map(str.strip, line.split('='))
            self.map[pos] = dict()

            left, right = re.match(r'\(([A-Z0-9]{3}), ([A-Z0-9]{3})\)', lr).groups()
            self.map[pos]['L'] = left
            self.map[pos]['R'] = right

    def part_1(self):
        pos = 'AAA'
        idx = 0

        while pos != 'ZZZ':
            self.add_result(1)

            ni = self.instructions[idx]
            if idx + 1 >= len(self.instructions):
                idx = 0
            else:
                idx += 1

            pos = self.map[pos][ni]

    def part_2(self):
        cycle_lengths = []

        for pos in self.map.keys():
            if not pos.endswith('A'):
                continue

            idx = 0
            counter = 0

            while not pos.endswith('Z'):
                counter += 1

                ni = self.instructions[idx]
                if idx + 1 >= len(self.instructions):
                    idx = 0
                else:
                    idx += 1

                pos = self.map[pos][ni]

            cycle_lengths.append(counter)

        return math.lcm(*cycle_lengths)


Day08(__file__).solve()

from shared.utils import *

from dataclasses import dataclass


@dataclass
class Position(object):
    x: int
    y: int


class Day14(Solution):
    cave: Grid
    max_y: int

    def setup(self):
        self.cave = Grid.empty(1000, 200).fill(' ')
        self.max_y = 0

        for line in self.input_lines():
            prev = None

            for coord in line.split(' -> '):
                x, y = map(int, coord.split(','))

                self.max_y = max(y, self.max_y)

                if prev is None:
                    prev = Position(x, y)
                    continue

                if x == prev.x:
                    for yi in range(min(y, prev.y), max(y, prev.y) + 1):
                        self.cave.set(x, yi, '#')
                elif y == prev.y:
                    for xi in range(min(x, prev.x), max(x, prev.x) + 1):
                        self.cave.set(xi, y, '#')

                prev = Position(x, y)

    def fill_sand(self):
        sp = Position(500, 0)  # sand position

        while sp.y < self.cave.height - 1:
            if self.cave.get(sp.x, sp.y + 1) == ' ':
                sp.y += 1
            elif self.cave.get(sp.x - 1, sp.y + 1) == ' ':
                sp.x -= 1
                sp.y += 1
            elif self.cave.get(sp.x + 1, sp.y + 1) == ' ':
                sp.x += 1
                sp.y += 1
            else:
                self.cave.set(sp.x, sp.y, 'o')

                if sp.x == 500 and sp.y == 0:
                    return  # filled up to start
                else:
                    sp = Position(500, 0)  # start new

    def part_1(self):
        self.fill_sand()
        # self.cave.print()
        return self.cave.count('o')

    def part_2(self):
        for x in range(self.cave.width):
            self.cave.set(x, self.max_y + 2, '#')

        self.fill_sand()
        # self.cave.print()
        return self.cave.count('o')


Day14(__file__).solve()

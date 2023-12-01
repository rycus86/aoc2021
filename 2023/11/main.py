import itertools

from shared.utils import *


class Day11(Solution):
    grid: Grid

    def setup(self):
        self.grid = self.input_grid()

    def part_1(self):
        self._collect_distances(gap_size=1)

    def part_2(self):
        self._collect_distances(gap_size=1000000-1)

    def _collect_distances(self, gap_size):
        empty_columns = list()
        for x in range(self.grid.width):
            if all(self.grid.get(x, y) == '.' for y in range(self.grid.height)):
                empty_columns.append(x)

        empty_rows = list()
        for y, row in enumerate(self.grid.rows):
            if '#' not in row:
                empty_rows.append(y)

        positions = list(self.grid.locate_all('#'))
        for (x1, y1), (x2, y2) in itertools.combinations(positions, 2):
            d = abs(x1 - x2) + abs(y1 - y2)

            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1

            for ex in empty_columns:
                if x1 < ex < x2:
                    d += gap_size

            for ey in empty_rows:
                if y1 < ey < y2:
                    d += gap_size

            self.add_result(d)


Day11(__file__).solve()

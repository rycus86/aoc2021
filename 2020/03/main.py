from shared.utils import *


class Day03(Solution):
    grid = Grid

    def setup(self):
        self.grid = self.input_grid()

    def part_1(self):
        return self.check_slope(3, 1)

    def part_2(self):
        total = 1
        for dx in (1, 3, 5, 7):
            total *= self.check_slope(dx, 1)
        total *= self.check_slope(1, 2)

        return total

    def check_slope(self, dx, dy):
        n_trees, x, y = 0, 0, 0
        while y < self.grid.height - 1:
            x, y = x + dx, y + dy
            if self.grid.get(x % self.grid.width, y) == '#':
                n_trees += 1

        return n_trees


Day03(__file__).solve()

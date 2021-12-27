from shared.utils import *


class Day11(Solution):
    grid: Grid

    def setup(self):
        self.grid = self.input_grid()

    def part_1(self):
        changed = True

        while changed:
            changed = False
            to_change = dict()

            for x in range(self.grid.width):
                for y in range(self.grid.height):
                    if self.grid.get(x, y) == 'L':
                        if not any('#' == item for item in self.grid.nearby_cells(x, y, True).values()):
                            to_change[(x, y)] = '#'
                            changed = True
                    elif self.grid.get(x, y) == '#':
                        if list(self.grid.nearby_cells(x, y, True).values()).count('#') >= 4:
                            to_change[(x, y)] = 'L'
                            changed = True

            for (x, y), target in to_change.items():
                self.grid.set(x, y, target)

        return self.grid.count('#')

    def part_2(self):
        changed = True
        dx_dy = tuple((dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx != 0 or dy != 0)

        while changed:
            changed = False
            to_change = dict()

            for x in range(self.grid.width):
                for y in range(self.grid.height):
                    cell = self.grid.get(x, y)
                    if cell == 'L':
                        any_occupied = False
                        for dx, dy in dx_dy:
                            if '#' == self.first_non_empty_towards(x, y, dx, dy):
                                any_occupied = True
                                break

                        if not any_occupied:
                            to_change[(x, y)] = '#'
                            changed = True

                    elif cell == '#':
                        number_of_occupied_seats = 0
                        for dx, dy in dx_dy:
                            if '#' == self.first_non_empty_towards(x, y, dx, dy):
                                number_of_occupied_seats += 1

                        if number_of_occupied_seats >= 5:
                            to_change[(x, y)] = 'L'
                            changed = True

            for (x, y), target in to_change.items():
                self.grid.set(x, y, target)

        return self.grid.count('#')

    def first_non_empty_towards(self, x, y, dx, dy):
        x, y = x + dx, y + dy

        while 0 <= x < self.grid.width and 0 <= y < self.grid.height:
            cell = self.grid.get(x, y)

            if cell != '.':
                return cell

            x, y = x + dx, y + dy


Day11(__file__).solve()

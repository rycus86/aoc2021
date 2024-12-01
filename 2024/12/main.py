from shared.utils import *


class Day12(Solution):
    grid: Grid
    plant_types: set[str]

    def setup(self):
        self.grid = self.input_grid()
        self.plant_types = set()

        for row in self.grid.rows:
            self.plant_types.update(set(row))

    def part_1(self):
        for pt in self.plant_types:
            grid = self.grid.clone(joining='')

            while location := grid.locate(pt):
                for x, y in grid.locate_all('*'):
                    grid.set(x, y, ' ')  # reset previous runs

                grid.flood_fill(location[0], location[1], pt, '*')
                area, perimeter = 0, 0
                for x, y in grid.locate_all('*'):
                    area += 1
                    perimeter += 4 - sum(1 if '*' == grid.get(nx, ny) else 0 for nx, ny in grid.nearby_cells(x, y))
                self.add_result(area * perimeter)

    def part_2(self):
        for pt in self.plant_types:

            grid = Grid.empty(self.grid.width + 2, self.grid.height + 2, default=' ')
            for ri, row in enumerate(self.grid.rows):
                for ci, value in enumerate(row):
                    grid.set_inplace(ci + 1, ri + 1, value)

            while location := grid.locate(pt):
                for x, y in grid.locate_all('*'):
                    grid.set(x, y, ' ')  # reset previous runs

                grid.flood_fill(location[0], location[1], pt, '*')
                area, sides = 0, list()
                for x, y in grid.locate_all('*'):
                    area += 1
                    for nx, ny in grid.nearby_cells(x, y):
                        if '*' != grid.get(nx, ny):
                            if nx == x:
                                sides.append((y - ny, 'y', x, y))
                            else:
                                sides.append((x - nx, 'x', x, y))

                # collapse sides (discard consecutive sides)
                new_side = 0
                for d in (1, -1):
                    for x in range(1, self.grid.width + 1):
                        added = False
                        for y in range(1, self.grid.height + 1):
                            if (d, 'x', x, y) in sides:
                                if not added:
                                    new_side += 1
                                    added = True
                            else:
                                added = False

                    for y in range(1, self.grid.height + 1):
                        added = False
                        for x in range(1, self.grid.width + 1):
                            if (d, 'y', x, y) in sides:
                                if not added:
                                    new_side += 1
                                    added = True
                            else:
                                added = False

                self.add_result(area * new_side)


Day12(__file__).solve()

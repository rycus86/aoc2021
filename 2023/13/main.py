from shared.utils import *


class Day13(Solution):
    grids: List[Grid]

    def setup(self):
        self.grids = list()

        rows = list()
        for row in self.input_lines():
            if not row.strip():
                self.grids.append(Grid(list(rows)))
                del rows[:]
            else:
                rows.append(row)
        else:
            self.grids.append(Grid(list(rows)))

    def part_1(self):
        for grid in self.grids:
            x, y = self._find_mirror(grid)
            if x is not None:
                self.add_result(x)
            else:
                self.add_result(100 * y)

    def part_2(self):
        for grid in self.grids:
            x, y = self._find_with_smudge(grid)
            if x:
                self.add_result(x)
            else:
                self.add_result(100 * y)

    def _find_mirror(self, grid: Grid, avoid=None):
        for x in range(1, grid.width):
            if avoid and avoid == (x, None):
                continue

            left = [grid.get_column(c) for c in range(x)]
            right = [grid.get_column(c) for c in range(x, grid.width)]
            if all(l == r for (l, r) in zip(reversed(left), right)):
                return x, None

        for y in range(1, grid.height):
            if avoid and avoid == (None, y):
                continue

            top = [grid.get_row(r) for r in range(y)]
            bottom = [grid.get_row(r) for r in range(y, grid.height)]
            if all(t == b for (t, b) in zip(reversed(top), bottom)):
                return None, y

        return None, None

    def _find_with_smudge(self, grid: Grid):
        ox, oy = self._find_mirror(grid)

        for cx in range(grid.width):
            for cy in range(grid.height):
                cloned = grid.clone()
                cloned.set(cx, cy, '.' if cloned.get(cx, cy) == '#' else '#')

                x, y = self._find_mirror(cloned, avoid=(ox, oy))
                if x is not None:
                    return x, None
                elif y is not None:
                    return None, y


Day13(__file__).solve()

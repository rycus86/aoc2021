from shared.utils import *


class Day08(Solution):
    grid: Grid
    frequencies: set[str]

    def setup(self):
        self.grid = self.input_grid()
        self.frequencies = {f for row in self.grid.rows for f in row} - {'.'}

    def _solve(self, part):
        results = set()

        for f in self.frequencies:
            locations = list(self.grid.locate_all(f))
            if part == 2:
                results.update(set(locations))

            for idx1 in range(len(locations) - 1):
                for idx2 in range(idx1 + 1, len(locations)):
                    x1, y1 = locations[idx1]
                    x2, y2 = locations[idx2]
                    dx, dy = x2 - x1, y2 - y1

                    a2, b2 = x2 + dx, y2 + dy
                    while 0 <= a2 < self.grid.width and 0 <= b2 < self.grid.height:
                        results.add((a2, b2))
                        if part == 1:
                            break
                        else:
                            a2 += dx
                            b2 += dy

                    a1, b1 = x1 - dx, y1 - dy
                    while 0 <= a1 < self.grid.width and 0 <= b1 < self.grid.height:
                        results.add((a1, b1))
                        if part == 1:
                            break
                        else:
                            a1 -= dx
                            b1 -= dy

        return len(results)

    def part_1(self):
        return self._solve(part=1)

    def part_2(self):
        return self._solve(part=2)


Day08(__file__).solve()

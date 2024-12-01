from shared.utils import *


class Day06(Solution):
    grid: Grid

    def setup(self):
        self.grid = self.input_grid()

    def _walk_grid(self, input_grid, visited_directions: dict[tuple[int, int], set[tuple[int]]] = None) -> tuple[Grid, bool]:
        grid = input_grid.clone(joining='')
        gx, gy = input_grid.locate('^')
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        current_direction = 0
        while True:
            if grid.get(gx, gy) == 'X' and visited_directions is not None:
                if current_direction in visited_directions[(gx, gy)]:
                    return grid, True
                else:
                    visited_directions[(gx, gy)].add(current_direction)
            else:
                grid.set(gx, gy, 'X')

            nx, ny = map(sum, zip([gx, gy], directions[current_direction]))
            if 0 <= nx < grid.width and 0 <= ny < grid.height:
                pass
            else:
                break

            if grid.get(nx, ny) == '#' or grid.get(nx, ny) == 'O':
                current_direction = (current_direction + 1) % len(directions)
            else:
                gx, gy = nx, ny

        return grid, False

    def part_1(self):
        grid, _ = self._walk_grid(self.grid)
        return grid.count('X')

    def part_2(self):
        sx, sy = self.grid.locate('^')
        route, _ = self._walk_grid(self.grid)
        for x, y in route.locate_all('X'):
            if (x, y) == (sx, sy):
                continue

            cloned = self.grid.clone()
            cloned.set(x, y, 'O')
            visited = defaultdict(set)
            _, reentered = self._walk_grid(cloned, visited)
            if reentered:
                self.add_result()


Day06(__file__).solve()

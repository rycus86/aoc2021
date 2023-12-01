from shared.utils import *


class Day16(Solution):
    grid: Grid

    def setup(self):
        self.grid = self.input_grid()

    def part_1(self):
        return self.check_from(0, 0, 1, 0)

    def part_2(self):
        winning = 0

        for y in range(self.grid.height):
            winning = max(winning, self.check_from(0, y, 1, 0))
            winning = max(winning, self.check_from(self.grid.width - 1, y, -1, 0))

        for x in range(self.grid.width):
            winning = max(winning, self.check_from(x, 0, 0, 1))
            winning = max(winning, self.check_from(x, self.grid.height - 1, 0, -1))

        return winning

    def check_from(self, fx, fy, fdx, fdy):
        energized = self.grid.clone(joining='')
        already_visited = set()

        steps = [(fx, fy, fdx, fdy)]
        while steps:
            x, y, dx, dy = steps.pop(0)
            if x < 0 or y < 0 or x >= self.grid.width or y >= self.grid.height:
                continue
            if (x, y, dx, dy) in already_visited:
                continue
            else:
                energized.set(x, y, '#')
                already_visited.add((x, y, dx, dy))

            steps.extend(self.step(x, y, dx, dy))

        return energized.count('#')

    def step(self, x, y, dx, dy) -> Iterable[Tuple[int, int, int, int]]:
        tile = self.grid.get(x, y)
        if tile == '.':
            yield x + dx, y + dy, dx, dy
        elif tile == '\\':
            if dx == 1:
                yield x, y + 1, 0, 1
            elif dx == -1:
                yield x, y - 1, 0, -1
            elif dy == 1:
                yield x + 1, y, 1, 0
            elif dy == -1:
                yield x - 1, y, -1, 0
        elif tile == '/':
            if dx == 1:
                yield x, y - 1, 0, -1
            elif dx == -1:
                yield x, y + 1, 0, 1
            elif dy == 1:
                yield x - 1, y, -1, 0
            elif dy == -1:
                yield x + 1, y, 1, 0
        elif tile == '-':
            if dy == 0:
                yield x + dx, y + dy, dx, dy
            else:
                yield x - 1, y, -1, 0
                yield x + 1, y, 1, 0
        elif tile == '|':
            if dx == 0:
                yield x + dx, y + dy, dx, dy
            else:
                yield x, y - 1, 0, -1
                yield x, y + 1, 0, 1


Day16(__file__).solve()

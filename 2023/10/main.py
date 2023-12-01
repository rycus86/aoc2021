from shared.utils import *


class Day10(Solution):
    grid: Grid

    def setup(self):
        self.grid = self.input_grid()

    def part_1(self):
        sx, sy = self.grid.locate('S')
        nx, ny = self._find_first_step()

        steps = 0

        px, py = sx, sy
        while (nx, ny) != (sx, sy):
            steps += 1
            px, py, (nx, ny) = nx, ny, self._next_step(px, py, nx, ny)

        return (steps + 1) // 2

    def _find_first_step(self):
        sx, sy = self.grid.locate('S')
        for (x, y), p in self.grid.nearby_cells(sx, sy).items():
            if y == sy:
                if p == '-':
                    return x, y
                elif x == sx - 1 and p in 'LF':
                    return x, y
                elif x == sx + 1 and p in 'J7':
                    return x, y
            elif x == sx:
                if p == '|':
                    return x, y
                elif y == sy - 1 and p in 'F7':
                    return x, y
                elif y == sy + 1 and p in 'LJ':
                    return x, y

    def _next_step(self, ax, ay, bx, by):
        p = self.grid.get(bx, by)
        if p == '|':
            if ay > by:
                return bx, by - 1
            else:
                return bx, by + 1
        elif p == '-':
            if ax > bx:
                return bx - 1, by
            else:
                return bx + 1, by
        elif p == 'L':
            if ax == bx:
                return bx + 1, by
            else:
                return bx, by - 1
        elif p == 'J':
            if ax == bx:
                return bx - 1, by
            else:
                return bx, by - 1
        elif p == '7':
            if ax == bx:
                return bx - 1, by
            else:
                return bx, by + 1
        elif p == 'F':
            if ax == bx:
                return bx + 1, by
            else:
                return bx, by + 1

    def part_2(self):
        self.grid = self._expand_grid()

        sx, sy = self.grid.locate('S')
        nx, ny = self._find_first_step()

        loop = [(sx, sy)]

        px, py = sx, sy
        while (nx, ny) != (sx, sy):
            loop.append((nx, ny))
            px, py, (nx, ny) = nx, ny, self._next_step(px, py, nx, ny)

        already_checked = set(loop)
        to_check = list()
        for x in range(self.grid.width):
            if (x, 0) not in loop:
                to_check.append((x, 0))
            if (x, self.grid.height - 1) not in loop:
                to_check.append((x, self.grid.height - 1))
        for y in range(self.grid.height):
            if (0, y) not in loop:
                to_check.append((0, y))
            if (self.grid.width - 1, y) not in loop:
                to_check.append((self.grid.width - 1, y))

        while len(to_check) > 0:
            x, y = to_check.pop(0)
            if (x, y) in already_checked:
                continue
            self.grid.set(x, y, 'O')
            already_checked.add((x, y))
            to_check.extend(self.grid.nearby_cells(x, y).keys())

        for lx, ly in loop:
            self.grid.set(lx, ly, '*')

        self.grid = self._shrink_grid()

        for rx in range(self.grid.width):
            for ry in range(self.grid.height):
                if self.grid.get(rx, ry) not in ' *O':
                    self.grid.set(rx, ry, 'I')

        # print()
        # self.grid.print()

        return self.grid.width * self.grid.height - self.grid.count('O') - self.grid.count('*')

    def _expand_grid(self):
        ng = Grid.empty(self.grid.width * 2, self.grid.height * 2)
        ng.fill('.')

        for ry, row in enumerate(self.grid.rows):
            for rx, rv in enumerate(row):
                ng.set(rx * 2, ry * 2, rv)
                if rv in '-LF':
                    ng.set(rx * 2 + 1, ry * 2, '-')
                if rv in '|7F':
                    ng.set(rx * 2, ry * 2 + 1, '|')
                if rx > 0 and rv in '-7J':
                    ng.set(rx * 2 - 1, ry * 2, '-')
                if ry > 0 and rv in '|LJ':
                    ng.set(rx * 2, ry * 2 - 1, '|')

        # ng.print()
        return ng

    def _shrink_grid(self):
        ng = Grid.empty(self.grid.width // 2, self.grid.height // 2)
        for x in range(ng.width):
            for y in range(ng.height):
                ng.set(x, y, self.grid.get(x * 2, y * 2))

        # ng.print()
        return ng


Day10(__file__).solve()

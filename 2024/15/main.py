from shared.utils import *


class Day15(Solution):
    grid: Grid
    moves: list[str]

    def _to_coord(self, m):
        if m == '<':
            return -1, 0
        elif m == '>':
            return 1, 0
        elif m == '^':
            return 0, -1
        elif m == 'v':
            return 0, 1

    def setup(self):
        g, m = self.input.split('\n\n')
        self.grid = Grid(g.splitlines(keepends=False))
        self.moves = list(map(self._to_coord, ''.join(m.splitlines(keepends=False))))

    def _move(self, sx, sy, dx, dy, just_check=False):
        tx, ty = sx + dx, sy + dy
        item = self.grid.get(tx, ty)

        if just_check and item == '.':
            return True

        if item == '#':
            return False

        elif item == 'O':
            if not self._move(tx, ty, dx, dy):
                return False

        elif item == '[':
            if dx == 0 and self._move(tx, ty, dx, dy, just_check=True) and self._move(tx + 1, ty, dx, dy, just_check=True):
                self._move(tx + 1, ty, dx, dy, just_check=just_check)
                self._move(tx, ty, dx, dy, just_check=just_check)
            elif dy == 0 and self._move(tx + 1, ty, dx, dy, just_check=True):
                self._move(tx + 1, ty, dx, dy)
                self._move(tx, ty, dx, dy)
            else:
                return False

        elif item == ']':
            if dx == 0 and self._move(tx, ty, dx, dy, just_check=True) and self._move(tx - 1, ty, dx, dy, just_check=True):
                self._move(tx - 1, ty, dx, dy, just_check=just_check)
                self._move(tx, ty, dx, dy, just_check=just_check)
            elif dy == 0 and self._move(tx - 1, ty, dx, dy, just_check=True):
                self._move(tx - 1, ty, dx, dy)
                self._move(tx, ty, dx, dy)
            else:
                return False

        if not just_check:
            source = self.grid.get(sx, sy)
            self.grid.set(tx, ty, source)
            self.grid.set(sx, sy, '.')

        return True

    def part_1(self):
        rx, ry = self.grid.locate('@')
        for mx, my in self.moves:
            if self._move(rx, ry, mx, my):
                rx, ry = rx + mx, ry + my

        # self.grid.print()

        for ox, oy in self.grid.locate_all('O'):
            self.add_result(100 * oy + ox)

    def part_2(self):
        # scale up
        new_rows = list()
        for row in self.grid.rows:
            new_row = ['.'] * len(row) * 2
            for idx, item in enumerate(row):
                if item == '#':
                    new_row[idx * 2], new_row[idx * 2 + 1] = '#', '#'
                elif item == 'O':
                    new_row[idx * 2], new_row[idx * 2 + 1] = '[', ']'
                elif item == '@':
                    new_row[idx * 2] = '@'
            new_rows.append(''.join(new_row))
        grid = Grid(new_rows)

        self.grid = grid

        rx, ry = self.grid.locate('@')
        for mx, my in self.moves:
            if self._move(rx, ry, mx, my):
                rx, ry = rx + mx, ry + my

            # self.grid.print()

        for ox, oy in self.grid.locate_all('['):
            self.add_result(100 * oy + ox)


Day15(__file__).solve()

from shared.utils import *
from functools import cache


class Day20(Solution):
    grid: Grid

    def setup(self):
        self.grid = self.input_grid()

    class Algo(Grid.Dijkstra):
        def neighbours(self, key):
            x, y, *_ = key
            for (nx, ny), value in self.grid.nearby_cells(x, y).items():
                if value == '.':
                    yield (nx, ny), 1

    def part_1(self):
        sx, sy = self.grid.locate('S')
        ex, ey = self.grid.locate('E')
        self.grid.set_inplace(ex, ey, '.')

        d = self.grid.dijkstra(algorithm=Day20.Algo, start_x=sx, start_y=sy)
        min_path = d.min_path(sx, sy, ex, ey)

        min_distance = self.grid.find_shortest_path(sx, sy, ex, ey)

        cheats = set()
        for px, py in min_path:
            for (wx, wy), item in self.grid.nearby_cells(px, py).items():
                if 0 < wx < self.grid.width - 1 and 0 < wy < self.grid.height - 1:
                    if item == '#':
                        dx, dy = px - wx, py - wy
                        wwx, wwy = wx + dx, wy + dy
                        wwi = self.grid.get(wwx, wwy)
                        if wwi == '.':
                            # valid single cheat
                            cheats.add((wx, wy, None, None))
                        elif wwi == '#':
                            if self.grid.get(wwx + dx, wwy + dy) == '.':
                                # valid double cheat
                                cheats.add((wx, wy, wwx, wwy))

        idx, total = 0, len(cheats)
        for ax, ay, bx, by in cheats:
            self.grid.set_inplace(ax, ay, '.')
            if bx is not None:
                self.grid.set_inplace(bx, by, '.')

            cheat_distance = self.grid.find_shortest_path(sx, sy, ex, ey, limit=min_distance - 99)

            if cheat_distance is not None and cheat_distance <= min_distance - 100:
                self.add_result()

            self.grid.set_inplace(ax, ay, '#')
            if bx is not None:
                self.grid.set_inplace(bx, by, '#')

            idx += 1
            # print(f'done: {idx}/{total}')

    def part_2(self):
        sx, sy = self.grid.locate('S')
        ex, ey = self.grid.locate('E')
        self.grid.set_inplace(ex, ey, '.')

        d = self.grid.dijkstra(algorithm=Day20.Algo, start_x=sx, start_y=sy)
        min_path = d.min_path(sx, sy, ex, ey)

        min_distance = self.grid.find_shortest_path(sx, sy, ex, ey)
        valid_cheats = 0

        for idx1, (x1, y1) in enumerate(min_path):
            for x2, y2 in min_path[idx1+1:]:
                if abs(x2 - x1) + abs(y2 - y1) <= 20:
                    new_score = idx1 + abs(x2 - x1) + abs(y2 - y1) + self._find_shortest_path(x2, y2, ex, ey)
                    if new_score <= min_distance - 100:
                        valid_cheats += 1

        return valid_cheats

    @cache
    def _find_shortest_path(self, sx, sy, tx, ty):
        return self.grid.find_shortest_path(sx, sy, tx, ty)


Day20(__file__).solve()

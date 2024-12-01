from shared.utils import *
import math


class Day16(Solution):
    grid: Grid

    def setup(self):
        self.grid = self.input_grid()

    def _calculate(self):
        sx, sy = self.grid.locate('S')
        tx, ty = self.grid.locate('E')
        dd = (1, 0)

        previous = defaultdict(set)
        score = dict()
        for x, y in self.grid.locate_all('.'):
            for d in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                score[(x, y, d)] = math.inf
        score[(sx, sy, dd)] = 0

        winning_score = math.inf
        winning_direction = None

        queue = list()
        heappush(queue, (0, (sx, sy, dd)))

        while queue:
            cost, key = heappop(queue)
            x, y, prev_dir = key

            for nx, ny in self.grid.nearby_cells(x, y):
                if self.grid.get(nx, ny) == '.':
                    next_dir = (nx - x, ny - y)
                    next_key = (nx, ny, next_dir)

                    if next_dir == prev_dir:
                        new_cost = cost + 1
                    elif next_dir == tuple(-1 * i for i in prev_dir):
                        new_cost = cost + 2000 + 1
                    else:
                        new_cost = cost + 1000 + 1

                    prev_score = score.get(next_key, math.inf)
                    if new_cost <= prev_score:
                        score[next_key] = new_cost
                        if new_cost < prev_score:
                            previous[(nx, ny, next_dir)] = {(x, y, prev_dir)}
                        else:
                            previous[(nx, ny, next_dir)].add((x, y, prev_dir))
                        heappush(queue, (new_cost, next_key))

                elif self.grid.get(nx, ny) == 'E':
                    next_dir = (nx - x, ny - y)
                    if next_dir == prev_dir:
                        new_cost = cost + 1
                    else:
                        new_cost = cost + 1000 + 1

                    if new_cost <= winning_score:
                        winning_score = new_cost
                        winning_direction = next_dir
                        if new_cost < winning_score:
                            previous[(nx, ny, next_dir)] = {(x, y, prev_dir)}
                        else:
                            previous[(nx, ny, next_dir)].add((x, y, prev_dir))

        path_queue = [(tx, ty, winning_direction)]
        while path_queue:
            x, y, d = path_queue.pop()
            self.grid.set(x, y, 'O')
            path_queue.extend(previous[(x, y, d)])

        return winning_score, self.grid.count('O')

    def part_1(self):
        lowest_score, _ = self._calculate()
        return lowest_score

    def part_2(self):
        _, best_tiles = self._calculate()
        return best_tiles


Day16(__file__).solve()

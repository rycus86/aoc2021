from shared.utils import *


class Day17(Solution):
    grid: Grid

    def setup(self):
        self.grid = Grid([list(map(int, row)) for row in self.input_lines()])

    class Algo(Grid.Dijkstra):
        directions = {
            'R': (1, 0),
            'L': (-1, 0),
            'D': (0, 1),
            'U': (0, -1)
        }
        opposites = {
            ('L', 'R'), ('R', 'L'),
            ('U', 'D'), ('D', 'U')
        }

        def __init__(self, grid: Grid, infinity, min_steps, max_steps):
            super().__init__(grid, infinity)
            self.min_steps = min_steps
            self.max_steps = max_steps

        def to_key(self, x, y):
            return x, y, '?', 0

        def neighbours(self, key):
            x, y, d, di = key

            for dd, (dx, dy) in self.directions.items():
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= self.grid.width:
                    continue
                if ny < 0 or ny >= self.grid.height:
                    continue

                if (d, dd) in self.opposites:
                    continue

                if dd == d:
                    ddi = di + 1
                    if ddi > self.max_steps:
                        continue
                elif d != '?' and di < self.min_steps:
                    continue
                else:
                    ddi = 1

                yield (nx, ny, dd, ddi), self.grid.get(nx, ny)

    def part_1(self):
        d = self.grid.dijkstra(algorithm=Day17.Algo, min_steps=1, max_steps=3)
        return d.min_distance()

    def part_2(self):
        d = self.grid.dijkstra(algorithm=Day17.Algo, min_steps=4, max_steps=10)
        return d.min_distance()


Day17(__file__).solve()

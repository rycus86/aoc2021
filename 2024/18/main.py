from shared.utils import *


class Day18(Solution):
    grid: Grid

    def setup(self):
        self.grid = Grid.empty(71, 71, default='.')

        for line in self.input_lines()[:1024]:
            x, y = map(int, line.split(','))
            self.grid.set(x, y, '#')

        # self.grid.print()

    class Algo(Grid.Dijkstra):
        def neighbours(self, key):
            x, y, *_ = key
            for (nx, ny), value in self.grid.nearby_cells(x, y).items():
                if value == '.':
                    yield (nx, ny), 1

    def part_1(self):
        d = self.grid.dijkstra(algorithm=Day18.Algo, start_x=0, start_y=0)
        return d.min_distance(self.grid.width - 1, self.grid.height - 1)

    def part_2(self):
        bits = list(tuple(map(int, line.split(','))) for line in self.input_lines()[1024:])
        low, high = 0, len(bits)

        while low < high:
            mid = (low + high) // 2
            grid = self.grid.clone()

            for x, y in bits[:mid]:
                grid.set(x, y, '#')

            d = grid.dijkstra(algorithm=Day18.Algo, start_x=0, start_y=0, infinity=math.inf)
            if math.inf == d.min_distance(grid.width - 1, grid.height - 1):
                high = mid - 1
            else:
                low = mid + 1

        x, y = bits[high]
        return f'{x},{y}'


Day18(__file__).solve()

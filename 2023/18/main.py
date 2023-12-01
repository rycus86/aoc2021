from shared.utils import *


class Day18(Solution):
    dig_plan: List[Tuple[str, int, str]]

    def setup(self):
        self.dig_plan = list()

        for line in self.input_lines():
            direction, amount, color = line.split()
            amount, color = int(amount), color[2:-1]
            self.dig_plan.append((direction, amount, color))

    def part_1(self):
        directions = {
            'R': (1, 0),
            'L': (-1, 0),
            'D': (0, 1),
            'U': (0, -1)
        }

        min_x, max_x, min_y, max_y = 0, 0, 0, 0
        x, y = 0, 0
        for d, a, _ in self.dig_plan:
            if d == 'R':
                x += a
                max_x = max(max_x, x)
            elif d == 'L':
                x -= a
                min_x = min(min_x, x)
            elif d == 'D':
                y += a
                max_y = max(max_y, y)
            elif d == 'U':
                y -= a
                min_y = min(min_y, y)

        width, height = max_x - min_x + 5, max_y - min_y + 5
        start_x, start_y = x - min_x, y - min_y

        grid = Grid.empty(width, height, default='.')

        x, y = start_x + 2, start_y + 2
        for d, a, _ in self.dig_plan:
            for p in range(a):
                x += directions[d][0]
                y += directions[d][1]
                grid.set(x, y, '#')

        grid.flood_fill(0, 0, '.', '*')

        return grid.count('#') + grid.count('.')

    def part_2(self):
        polygon = Polygon()
        directions = {
            'R': (1, 0),
            'L': (-1, 0),
            'D': (0, 1),
            'U': (0, -1)
        }

        x, y = 0, 0
        for idx, (d, a, c) in enumerate(self.dig_plan):
            ca, cd = c[:5], c[-1]
            ca, cd = int(ca, base=16), 'RDLU'[int(cd)]
            self.dig_plan[idx] = (cd, ca, '')

            nx, ny = directions[cd]

            x2, y2 = x + nx * ca, y + ny * ca
            polygon.add_edge(Side(x, y, x2, y2))
            x, y = x2, y2

        return polygon.calculate_area()


class Side:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def length(self):
        return abs(self.x1 - self.x2) + abs(self.y1 - self.y2)

    def __repr__(self):
        return f'S({self.x1}x{self.y1}->{self.x2}x{self.y2})'


class Polygon:
    edges: List[Side]

    def __init__(self):
        self.edges = list()
        self.corners_x = set()
        self.corners_y = set()

        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

    def add_edge(self, side: Side):
        self.edges.append(side)
        self.corners_x.add(side.x1)
        self.corners_x.add(side.x2)
        self.corners_y.add(side.y1)
        self.corners_y.add(side.y2)

        self.min_x = min(self.min_x, side.x1)
        self.min_x = min(self.min_x, side.x2)
        self.max_x = max(self.max_x, side.x1)
        self.max_x = max(self.max_x, side.x2)
        self.min_y = min(self.min_y, side.y1)
        self.min_y = min(self.min_y, side.y2)
        self.max_y = max(self.max_y, side.y1)
        self.max_y = max(self.max_y, side.y2)

    def calculate_area(self):
        total_area = 0
        length = 0

        for e in self.edges:
            total_area += e.x1 * e.y2 - e.x2 * e.y1
            length += e.length()

        return total_area // 2 + length // 2 + 1

    def __repr__(self):
        return f'P{self.edges}'


Day18(__file__).solve()

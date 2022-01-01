from shared.utils import *


class Line(object):
    def __init__(self, x1, y1, x2, y2, d):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.d = d

    def intersection(self, o) -> Tuple[int, int, int]:
        sx1, sy1, sx2, sy2 = min(self.x1, self.x2), min(self.y1, self.y2), max(self.x1, self.x2), max(self.y1, self.y2)
        ox1, oy1, ox2, oy2 = min(o.x1, o.x2), min(o.y1, o.y2), max(o.x1, o.x2), max(o.y1, o.y2)

        if sx1 == sx2 and oy1 == oy2:
            if ox1 <= sx1 <= ox2 and sy1 <= oy1 <= sy2:
                return sx1, oy1, self.d + o.d + abs(self.x1 - o.x1) + abs(o.y1 - self.y1)

        elif sy1 == sy2 and ox1 == ox2:
            if sx1 <= ox1 <= sx2 and oy1 <= sy1 <= oy2:
                return ox1, sy1, self.d + o.d + abs(o.x1 - self.x1) + abs(self.y1 - o.y1)

        return None, None, None


class Day03(Solution):
    wire1: List[Line]
    min_distance: int

    def part_1(self):
        return self.evaluate(part=1)

    def part_2(self):
        return self.evaluate(part=2)

    def evaluate(self, part: int):
        self.wire1 = list()
        self.min_distance = 10 ** 12

        x, y, d = 0, 0, 0

        for item in self.input_lines()[0].split(','):
            direction, value = item[0], int(item[1:])
            if direction == 'U':
                self.wire1.append(Line(x, y, x, y + value, d))
                y += value
            elif direction == 'D':
                self.wire1.append(Line(x, y, x, y - value, d))
                y -= value
            elif direction == 'L':
                self.wire1.append(Line(x, y, x - value, y, d))
                x -= value
            elif direction == 'R':
                self.wire1.append(Line(x, y, x + value, y, d))
                x += value

            d += value

        x, y, d = 0, 0, 0

        for item in self.input_lines()[1].split(','):
            direction, value = item[0], int(item[1:])
            if direction == 'U':
                self.check_intersection(Line(x, y, x, y + value, d), part)
                y += value
            elif direction == 'D':
                self.check_intersection(Line(x, y, x, y - value, d), part)
                y -= value
            elif direction == 'L':
                self.check_intersection(Line(x, y, x - value, y, d), part)
                x -= value
            elif direction == 'R':
                self.check_intersection(Line(x, y, x + value, y, d), part)
                x += value

            d += value

        return self.min_distance

    def check_intersection(self, line: Line, part: int):
        for w1 in self.wire1:
            i, j, d = w1.intersection(line)
            if i or j:
                if part == 1:
                    self.min_distance = min(abs(i) + abs(j), self.min_distance)
                else:
                    self.min_distance = min(d, self.min_distance)


Day03(__file__).solve()

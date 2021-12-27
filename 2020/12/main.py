from shared.utils import *


class Day12(Solution):
    x: int
    y: int
    dx: int
    dy: int
    instructions: List[Tuple[str, int]]

    def setup(self):
        self.x, self.y = 0, 0
        self.dx, self.dy = 1, 0
        self.instructions = [(item[0], int(item[1:])) for item in self.input_lines()]

    def part_1(self):
        for action, value in self.instructions:
            self.move(action, value)

        return abs(self.x) + abs(self.y)

    def part_2(self):
        self.dx, self.dy = 10, -1

        for action, value in self.instructions:
            self.move(action, value, True)

        return abs(self.x) + abs(self.y)

    def move(self, action, value, is_part2=False):
        if action == 'N':
            if is_part2:
                self.dy -= value
            else:
                self.y -= value
        elif action == 'S':
            if is_part2:
                self.dy += value
            else:
                self.y += value
        elif action == 'W':
            if is_part2:
                self.dx -= value
            else:
                self.x -= value
        elif action == 'E':
            if is_part2:
                self.dx += value
            else:
                self.x += value
        elif action == 'L':
            assert value in (90, 180, 270)
            if value == 90:
                self.dx, self.dy = self.dy, -self.dx
            elif value == 180:
                self.dx, self.dy = -self.dx, -self.dy
            elif value == 270:
                self.move('R', 90)
        elif action == 'R':
            assert value in (90, 180, 270)
            if value == 90:
                self.dx, self.dy = -self.dy, self.dx
            elif value == 180:
                self.dx, self.dy = -self.dx, -self.dy
            elif value == 270:
                self.move('L', 90)
        elif action == 'F':
            self.x += value * self.dx
            self.y += value * self.dy


Day12(__file__).solve()

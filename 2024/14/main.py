from shared.utils import *
from dataclasses import dataclass
import os


@dataclass
class Robot:
    gx = 101
    gy = 103
    mx = gx // 2
    my = gy // 2

    px: int
    py: int
    vx: int
    vy: int

    def move(self):
        self.px = (self.px + self.vx) % self.gx
        self.py = (self.py + self.vy) % self.gy

    def quadrant(self):
        if self.px == self.mx or self.py == self.my:
            return None

        qx = 'L' if self.px < self.mx else 'R'
        qy = 'T' if self.py < self.my else 'B'
        return qx, qy


class Day14(Solution):
    robots: list[Robot]

    def setup(self):
        self.robots = list()

        for line in self.input_lines():
            p, v = line.split()
            px, py = map(int, p.split('=')[1].split(','))
            vx, vy = map(int, v.split('=')[1].split(','))
            self.robots.append(Robot(px, py, vx, vy))

    def part_1(self):
        for _ in range(100):
            for robot in self.robots:
                robot.move()

        quadrants = defaultdict(int)
        for robot in self.robots:
            quadrants[robot.quadrant()] += 1

        if None in quadrants:
            del quadrants[None]

        return var_mul(*list(c for k, c in quadrants.items() if k is not None))

    def part_2(self):
        steps = 0
        for _ in range(10000):
            steps += 1
            grid = Grid.empty(Robot.gx, Robot.gy, ' ')

            for robot in self.robots:
                robot.move()
                grid.set(robot.px, robot.py, '*')

            for row in grid.rows:
                # print if there are at least 10 robots next to each other on the same row
                if row.count('*') > 10:
                    if '*' * 10 in ''.join(row):
                        grid.print()
                        return steps


Day14(__file__).solve()

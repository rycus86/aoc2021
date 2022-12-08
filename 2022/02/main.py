from shared.utils import *


class Day02(Solution):
    shapes = {
        'A': 1,
        'B': 2,
        'C': 3,
        'X': 1,
        'Y': 2,
        'Z': 3
    }

    def setup(self):
        pass

    def part_1(self):
        for line in self.input_lines():
            a, b = (self.shapes[x] for x in line.split())
            self.add_result(self.check_points(a, b))

    def part_2(self):
        for line in self.input_lines():
            a, b = line.split()
            a = self.shapes[a]

            if b == 'Y':  # draw
                b = a
            elif b == 'X':  # lose
                b = (a - 1) if a > 1 else 3
            elif b == 'Z':  # win
                b = (a + 1) if a < 3 else 1

            self.add_result(self.check_points(a, b))

    @staticmethod
    def check_points(a, b):
        if (a, b) in ((1, 2), (2, 3), (3, 1)):
            return b + 6
        elif a == b:
            return b + 3
        else:
            return b


Day02(__file__).solve()

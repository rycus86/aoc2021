from shared.utils import *


class Day04(Solution):
    x: int
    y: int

    def setup(self):
        self.x, self.y = map(int, self.input.split('-'))

    def part_1(self):
        self.check(part=1)

    def part_2(self):
        self.check(part=2)

    def check(self, part):
        for a in range(self.x // 10**5, self.y // 10**5 + 1):
            for b in range(a, 10):
                for c in range(b, 10):
                    for d in range(c, 10):
                        for e in range(d, 10):
                            for f in range(e, 10):
                                concatenated = f'{a}{b}{c}{d}{e}{f}'
                                parsed = int(concatenated)

                                if self.x <= parsed <= self.y and len(set(concatenated)) < 6:
                                    if part == 1:
                                        self.add_result()

                                    elif part == 2 and any(concatenated.count(str(i)) == 2 for i in range(1, 10)):
                                        self.add_result()


Day04(__file__).solve()

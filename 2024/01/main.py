from shared.utils import *


class Day01(Solution):
    a: List[int]
    b: List[int]

    def setup(self):
        self.a = list()
        self.b = list()

        for line in self.input_lines():
            a, b = map(int, line.split())
            self.a.append(a)
            self.b.append(b)

    def part_1(self):
        a = list(sorted(self.a))
        b = list(sorted(self.b))

        for idx in range(len(a)):
            self.add_result(abs(a[idx] - b[idx]))

    def part_2(self):
        appearances = defaultdict(int)
        for b in self.b:
            appearances[b] += 1

        for a in self.a:
            self.add_result(a * appearances[a])


Day01(__file__).solve()

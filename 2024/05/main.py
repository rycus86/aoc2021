import functools
from shared.utils import *


class Day05(Solution):
    index: dict[tuple[int, int], int]
    pages: list[list[int]]
    sorted_pages: list[list[int]]

    def setup(self):
        self.index = dict()
        self.pages = list()
        self.sorted_pages = list()

        for line in self.input_lines():
            if '|' in line:
                a, b = map(int, line.split('|'))
                self.index[(a, b)] = -1
                self.index[(b, a)] = 1
            elif ',' in line:
                self.pages.append(list(map(int, line.split(','))))

        for page in self.pages:
            self.sorted_pages.append(sorted(page, key=functools.cmp_to_key(self._compare)))

    def _compare(self, a, b):
        return self.index.get((a, b), 0)

    def part_1(self):
        for a, b in zip(self.pages, self.sorted_pages):
            if a == b:
                self.add_result(b[len(b) // 2])

    def part_2(self):
        for a, b in zip(self.pages, self.sorted_pages):
            if a != b:
                self.add_result(b[len(b) // 2])


Day05(__file__).solve()

import functools

from shared.utils import *


class Coords(list):
    def __hash__(self):
        return hash(tuple(self))


class Day22(Solution):
    bricks: List[Tuple[Coords[int], Coords[int]]]
    above: Dict
    under: Dict

    def setup(self):
        self.bricks = list()

        for line in self.input_lines():
            left, right = line.split('~')
            left, right = Coords(map(int, left.split(','))), Coords(map(int, right.split(',')))
            self.bricks.append((left, right))

        floor = defaultdict(int)  # z at (x, y)

        for brick in sorted(self.bricks, key=lambda i: min(i[0][-1], i[1][-1])):
            bottom = max(floor[(x, y)] + 1
                         for x in range(brick[0][0], brick[1][0] + 1)
                         for y in range(brick[0][1], brick[1][1] + 1))

            height = brick[1][2] - brick[0][2]
            brick[0][2] = bottom
            brick[1][2] = bottom + height

            for x in range(brick[0][0], brick[1][0] + 1):
                for y in range(brick[0][1], brick[1][1] + 1):
                    floor[(x, y)] = bottom + height

        self.above, self.under = defaultdict(set), defaultdict(set)
        for idx, brick in enumerate(self.bricks):
            bz1, bz2 = brick[0][-1], brick[1][-1]
            bxy = set((x, y)
                      for x in range(brick[0][0], brick[1][0] + 1)
                      for y in range(brick[0][1], brick[1][1] + 1))

            for other in self.bricks[idx+1:]:
                oz1, oz2 = other[0][-1], other[1][-1]

                if bz2 + 1 == oz1:  # brick is under other
                    a, u = brick, other
                elif oz2 + 1 == bz1:  # brick is above other
                    a, u = other, brick
                else:
                    continue

                if not any((x, y) in bxy
                           for x in range(other[0][0], other[1][0] + 1)
                           for y in range(other[0][1], other[1][1] + 1)):
                    continue  # no overlap

                self.above[a].add(u)
                self.under[u].add(a)

    def part_1(self):
        for brick in self.bricks:
            # safe to disintegrate if all bricks above this one have another one to support them
            if all(len(self.under[other]) > 1 for other in self.above[brick]):
                self.add_result()

    def part_2(self):
        @functools.cache
        def others_that_would_fall(*gone):
            others, gs = set(), set(gone)
            for b in gone:
                for other in self.above[b]:
                    if other in gs:
                        continue  # already dealt with

                    # it would fall if all bricks under it have already fallen
                    if all(u in gone for u in self.under[other]):
                        others.add(other)

            if others:
                others.update(others_that_would_fall(*gone, *others))

            return others

        for brick in self.bricks:
            self.add_result(len(others_that_would_fall(brick)))


Day22(__file__).solve()

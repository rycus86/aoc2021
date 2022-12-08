from shared.utils import *

import re
from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Interval:
    x1: int
    x2: int


class Day15(Solution):
    sensors: Dict[Position, Position]
    beacons: Dict[Position, List[Position]]

    def setup(self):
        self.sensors = dict()
        self.beacons = dict()

        pattern = re.compile(r'Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)')

        for line in self.input_lines():
            sx, sy, bx, by = map(int, pattern.match(line).groups())
            s, b = Position(sx, sy), Position(bx, by)

            self.sensors[s] = b

            if b in self.beacons:
                self.beacons[b].append(s)
            else:
                self.beacons[b] = [s]

    def part_1(self):
        row = 2000000
        positions = set()

        for s, b in self.sensors.items():
            md = abs(s.x - b.x) + abs(s.y - b.y)  # distance of beacon
            if abs(s.y - row) < md:
                for x in range(s.x - (md - abs(s.y - row)), s.x + (md - abs(s.y - row)) + 1):
                    positions.add(x)

        for b in self.beacons:
            if b.y == row:
                if b.x in positions:
                    positions.remove(b.x)

        for s in self.sensors:
            if s.y == row:
                if s.x in positions:
                    positions.remove(s.x)

        return len(positions)

    def part_2(self):
        for row in range(4000000):
            intervals = list()

            for s, b in self.sensors.items():
                md = abs(s.x - b.x) + abs(s.y - b.y)  # distance of beacon
                rx = md - abs(s.y - row)
                if rx > 0:
                    x1, x2 = max(0, min(4000000, s.x - rx)), max(0, min(4000000, s.x + rx))
                    added = False

                    for i in intervals:
                        if x1 < i.x1 < x2:
                            i.x1 = x1
                            added = True
                        elif x1 < i.x2 < x2:
                            i.x2 = x2
                            added = True

                    if not added:
                        intervals.append(Interval(x1, x2))

            intervals.sort(key=lambda item: (item.x1, item.x2))

            def find_contained():
                for idx1, i1 in enumerate(intervals):
                    for idx2, i2 in enumerate(intervals):
                        if idx1 == idx2:
                            continue

                        if i1.x1 <= i2.x1 and i1.x2 >= i2.x2:
                            return idx2

            c = find_contained()
            while c is not None:
                del intervals[c]
                c = find_contained()

            def find_overlapping():
                for idx1, i1 in enumerate(intervals):
                    for idx2, i2 in enumerate(intervals):
                        if idx1 == idx2:
                            continue

                        if i1.x1 <= i2.x1 <= i1.x2:
                            return idx1, idx2, min(i1.x1, i2.x1), max(i1.x2, i2.x2)
                        elif i1.x1 <= i2.x2 <= i1.x2:
                            return idx1, idx2, min(i1.x1, i2.x1), max(i1.x2, i2.x2)

                return [None] * 4

            idx1, idx2, x1, x2 = find_overlapping()
            while idx1 is not None:
                intervals[idx1].x1 = x1
                intervals[idx1].x2 = x2
                del intervals[idx2]
                idx1, idx2, x1, x2 = find_overlapping()

            if len(intervals) == 2:
                if intervals[1].x1 - intervals[0].x2 == 2:
                    return 4000000 * (intervals[0].x2 + 1) + row


Day15(__file__).solve()

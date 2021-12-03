def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


class Range(object):
    def __init__(self, x1, x2, y1, y2, z1, z2, control_on=True):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        self.control_on = control_on

    def __lt__(self, other):
        return self.area() < other.area()

    def __repr__(self):
        return f'[{self.x1},{self.y1},{self.z1}]->[{self.x2},{self.y2},{self.z2}]'

    def __str__(self):
        return repr(self)

    def area(self):
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1) * (self.z2 - self.z1 + 1)

    def split(self, other_range):
        # after a lot of trial and error, this solution gave me the hints I needed in the end:
        #   https://github.com/davearussell/advent2021/blob/master/day22/solve.py

        bx1, bx2 = other_range.x1, other_range.x2
        by1, by2 = other_range.y1, other_range.y2
        bz1, bz2 = other_range.z1, other_range.z2

        if self.x2 < bx1 or bx2 < self.x1:
            yield self
        elif self.y2 < by1 or by2 < self.y1:
            yield self
        elif self.z2 < bz1 or bz2 < self.z1:
            yield self

        elif self.x1 < bx1:
            yield Range(self.x1, bx1 - 1, self.y1, self.y2, self.z1, self.z2)

            if self.x2 > bx2:
                for mr in Range(bx1, bx2, self.y1, self.y2, self.z1, self.z2).split(other_range):
                    yield mr
                yield Range(bx2 + 1, self.x2, self.y1, self.y2, self.z1, self.z2)
            else:
                for mr in Range(bx1, self.x2, self.y1, self.y2, self.z1, self.z2).split(other_range):
                    yield mr

        elif self.x2 > bx2:
            for mr in Range(self.x1, bx2, self.y1, self.y2, self.z1, self.z2).split(other_range):
                yield mr
            yield Range(bx2 + 1, self.x2, self.y1, self.y2, self.z1, self.z2)

        elif self.y1 < by1:
            yield Range(self.x1, self.x2, self.y1, by1 - 1, self.z1, self.z2)

            if self.y2 > by2:
                for mr in Range(self.x1, self.x2, by1, by2, self.z1, self.z2).split(other_range):
                    yield mr
                yield Range(self.x1, self.x2, by2 + 1, self.y2, self.z1, self.z2)
            else:
                for mr in Range(self.x1, self.x2, by1, self.y2, self.z1, self.z2).split(other_range):
                    yield mr

        elif self.y2 > by2:
            for mr in Range(self.x1, self.x2, self.y1, by2, self.z1, self.z2).split(other_range):
                yield mr
            yield Range(self.x1, self.x2, by2 + 1, self.y2, self.z1, self.z2)

        elif self.z1 < bz1:
            yield Range(self.x1, self.x2, self.y1, self.y2, self.z1, bz1 - 1)

            if self.z2 > bz2:
                for mr in Range(self.x1, self.x2, self.y1, self.y2, bz1, bz2).split(other_range):
                    yield mr
                yield Range(self.x1, self.x2, self.y1, self.y2, bz2 + 1, self.z2)
            else:
                for mr in Range(self.x1, self.x2, self.y1, self.y2, bz1, self.z2).split(other_range):
                    yield mr

        elif self.z2 > bz2:
            for mr in Range(self.x1, self.x2, self.y1, self.y2, self.z1, bz2).split(other_range):
                yield mr
            yield Range(self.x1, self.x2, self.y1, self.y2, bz2 + 1, self.z2)


if __name__ == '__main__':
    ranges_on = set()

    for line in read_input().splitlines():
        on_off, line = line.split(' ')
        x, y, z = line.split(',')
        x1, x2 = map(int, x[2:].split('..'))
        y1, y2 = map(int, y[2:].split('..'))
        z1, z2 = map(int, z[2:].split('..'))

        r = Range(x1, x2, y1, y2, z1, z2, on_off == 'on')
        new_ranges = set()

        for e in set(ranges_on):
            for s in e.split(r):
                new_ranges.add(s)

        if r.control_on:
            new_ranges.add(r)

        ranges_on = new_ranges

    print('result:', sum(r.area() for r in ranges_on))

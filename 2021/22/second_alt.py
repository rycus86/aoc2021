def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


class Range(object):
    def __init__(self, x1, x2, y1, y2, z1, z2, control_on=False):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        self.control_on = control_on

    def __repr__(self):
        return f'[{self.x1},{self.y1},{self.z1}]->[{self.x2},{self.y2},{self.z2}]'

    def area(self):
        return (1 if self.control_on else -1) * \
               (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1) * (self.z2 - self.z1 + 1)

    def intersection(self, other):
        result = Range(max(self.x1, other.x1), min(self.x2, other.x2),
                       max(self.y1, other.y1), min(self.y2, other.y2),
                       max(self.z1, other.z1), min(self.z2, other.z2),
                       self.control_on)
        if result.x1 <= result.x2 and result.y1 <= result.y2 and result.z1 <= result.z2:
            return result
        else:
            return

    def invert(self):
        self.control_on = not self.control_on
        return self


if __name__ == '__main__':
    ranges_on = list()

    for line in read_input().splitlines():
        on_off, line = line.split(' ')
        x, y, z = line.split(',')
        x1, x2 = map(int, x[2:].split('..'))
        y1, y2 = map(int, y[2:].split('..'))
        z1, z2 = map(int, z[2:].split('..'))

        # initially tried splitting regions, similar to this solution:
        #   https://github.com/davearussell/advent2021/blob/master/day22/solve.py
        #   but I couldn't get it working properly
        # this solution below is based on the idea from Reddit:
        #   https://old.reddit.com/r/adventofcode/comments/rlxhmg/2021_day_22_solutions/hpizza8/

        current = Range(x1, x2, y1, y2, z1, z2, on_off == 'on')
        new_ranges = list()

        for existing in ranges_on:
            # check if the current cube affects an existing one
            intersection = existing.intersection(current)
            if intersection:
                # if it was a cube on, add the intersection the cancels it off
                # if it was off, add a cube that turns it back on,
                #   because there must be a cube that was on before,
                #   and we'll subtract from that one (e.g. turn it off)
                new_ranges.append(intersection.invert())

        if current.control_on:
            # if this cube is on, add it,
            #   so it'll be a positive sum in the result
            new_ranges.append(current)

        ranges_on.extend(new_ranges)

    print('result:', sum(r.area() for r in ranges_on))

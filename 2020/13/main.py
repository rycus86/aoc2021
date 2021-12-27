from shared.utils import *


class Day13(Solution):
    earliest: int
    buses: List[Tuple[int, int]]

    def setup(self):
        self.earliest = int(self.input_lines()[0])
        self.buses = [(int(bus), idx) for idx, bus in enumerate(self.input_lines()[1].split(',')) if bus != 'x']

    def part_1(self):
        target = (max(b for b, _ in self.buses) + 1, 0)

        for bus, _ in self.buses:
            departs_in = bus - self.earliest % bus
            if target[0] > departs_in:
                target = (departs_in, bus)

        return target[0] * target[1]

    def part_2(self):
        first_bus, _ = self.buses[0]

        value = 0
        to_add = first_bus

        for bus, idx in self.buses[1:]:
            target = bus - idx
            while target < 0:
                target += bus

            while value % bus != target:
                value += to_add
            else:
                to_add *= bus

        return value


Day13(__file__).solve()

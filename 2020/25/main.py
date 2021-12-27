from shared.utils import *


class Day25(Solution):
    pk_card: int
    pk_door: int

    def setup(self):
        self.pk_card = int(self.input_lines()[0])
        self.pk_door = int(self.input_lines()[1])

    def part_1(self):
        loop_card = self.loop_size(self.pk_card)
        loop_door = self.loop_size(self.pk_door)

        key1 = self.transform(self.pk_door, loop_card)
        key2 = self.transform(self.pk_card, loop_door)

        assert key1 == key2

        return key1

    def loop_size(self, public_key):
        value = 1
        for loop in range(100000000):
            value = (value * 7) % 20201227
            if value == public_key:
                return loop + 1

    def transform(self, subject_number, loops):
        value = 1
        for loop in range(loops):
            value = (value * subject_number) % 20201227
        return value

    def part_2(self):
        pass  # no part two on day 25


Day25(__file__).solve()

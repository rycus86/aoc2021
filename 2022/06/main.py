from shared.utils import *


class Day06(Solution):
    signal: str

    def setup(self):
        self.signal = self.input_lines()[0]

    def part_1(self):
        return self.detect(marker_length=4)

    def part_2(self):
        return self.detect(marker_length=14)

    def detect(self, marker_length):
        pos = marker_length
        while pos < len(self.signal):
            if len(set(self.signal[pos-marker_length:pos])) == marker_length:
                return pos
            else:
                pos += 1


Day06(__file__).solve()

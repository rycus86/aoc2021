import re

from shared.utils import *


class Day01(Solution):
    num_mappings = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9
    }

    def part_1(self):
        for line in self.input_lines():
            digits_only, _ = re.subn('[^0-9]', '', line)
            self.add_result(int(digits_only[0] + digits_only[-1]))

    def part_2(self):
        for line in self.input_lines():
            original = line

            for key, digit in self.num_mappings.items():
                line = line.replace(str(digit), key)

            min_digit, min_key, min_pos = None, None, len(line) + 1
            for key, digit in self.num_mappings.items():
                pos = line.find(key)
                if -1 < pos < min_pos:
                    min_digit, min_key, min_pos = str(digit), key, pos

            if min_digit:
                line = line[:min_pos] + min_digit + line[min_pos + len(min_key):]

            max_digit, max_key, max_pos = None, None, -1
            for key, digit in self.num_mappings.items():
                pos = line.rfind(key)
                if pos > max_pos:
                    max_digit, max_key, max_pos = str(digit), key, pos

            if max_digit:
                line = line[:max_pos] + max_digit + line[max_pos + len(max_key):]

            digits_only, _ = re.subn('[^0-9]', '', line)
            self.add_result(int(digits_only[0] + digits_only[-1]))


Day01(__file__).solve()

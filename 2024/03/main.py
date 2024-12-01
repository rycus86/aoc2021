import re

from shared.utils import *


class Day03(Solution):

    def part_1(self):
        for match in re.finditer(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)', self.input):
            self.add_result(int(match.group(1)) * int(match.group(2)))

    def part_2(self):
        enabled = True
        for match in re.finditer(r"(do)\(\)|(don't)\(\)|mul\(([0-9]{1,3}),([0-9]{1,3})\)", self.input):
            if match.group(1) == 'do':
                enabled = True
            elif match.group(2) == "don't":
                enabled = False
            elif enabled:
                self.add_result(int(match.group(3)) * int(match.group(4)))


Day03(__file__).solve()

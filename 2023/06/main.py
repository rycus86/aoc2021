import re

from shared.utils import *


class Day06(Solution):
    times: List[int]
    distances: List[int]

    def setup(self):
        for line in self.input_lines():
            if line.startswith('Time:'):
                line = line.replace('Time:', '').strip()
                line, _ = re.subn(r'\s+', ' ', line)
                self.times = list(map(int, line.split(' ')))
            elif line.startswith('Distance:'):
                line = line.replace('Distance:', '').strip()
                line, _ = re.subn(r'\s+', ' ', line)
                self.distances = list(map(int, line.split(' ')))

    def part_1(self):
        solution = 1

        for idx in range(len(self.times)):
            total_time, current_record = self.times[idx], self.distances[idx]

            ways = 0
            for hold in range(total_time):
                result = hold * (total_time - hold)
                if result > current_record:
                    ways += 1

            solution *= ways

        return solution

    def part_2(self):
        total_time = int(''.join(map(str, self.times)))
        current_record = int(''.join(map(str, self.distances)))

        ways = 0
        for hold in range(total_time):
            result = hold * (total_time - hold)
            if result > current_record:
                ways += 1

        return ways


Day06(__file__).solve()

from shared.utils import *


class Day02(Solution):

    def setup(self):
        pass

    def part_1(self):
        for line in self.input_lines():
            if self._check_line(list(map(int, line.split())), allow_adjustment=False):
                self.add_result()

    def part_2(self):
        for line in self.input_lines():
            if self._check_line(list(map(int, line.split())), allow_adjustment=True):
                self.add_result()


    def _check_line(self, values, allow_adjustment=False):
        last_level = None
        direction = None
        for level in values:
            if last_level is None:
                last_level = level
            else:
                if direction is None:
                    direction = last_level > level
                else:
                    new_direction = last_level > level
                    if new_direction != direction:
                        break

                if 1 <= abs(last_level - level) <= 3:
                    last_level = level
                else:
                    break
        else:
            return True

        if allow_adjustment:
            for idx in range(len(values)):
                if self._check_line(values[0:idx] + values[idx + 1:]):
                    return True


Day02(__file__).solve()

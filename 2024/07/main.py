from shared.utils import *


class Day07(Solution):
    calibrations: list[tuple[int, list[int]]]

    def setup(self):
        self.calibrations = list()

        for line in self.input_lines():
            result, items = map(str.strip, line.split(':'))
            result, items = int(result), list(map(int, items.split()))
            self.calibrations.append((result, items))

    def _check_result(self, result: int, items: list[int], part: int) -> bool:
        if len(items) > 2:
            return any((
                self._check_result(result, [items[0] + items[1]] + items[2:], part),
                self._check_result(result, [items[0] * items[1]] + items[2:], part),
                self._check_result(result, [int(str(items[0]) + str(items[1]))] + items[2:], part) if part == 2 else False
            ))
        else:
            return result in (
                items[0] + items[1],
                items[0] * items[1],
                int(str(items[0]) + str(items[1])) if part == 2 else -1
            )

    def part_1(self):
        for result, items in self.calibrations:
            if self._check_result(result, items, part=1):
                self.add_result(result)

    def part_2(self):
        for result, items in self.calibrations:
            if self._check_result(result, items, part=2):
                self.add_result(result)


Day07(__file__).solve()

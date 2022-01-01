from shared.utils import *


class Day02(Solution):
    numbers: List[int]

    def setup(self):
        self.numbers = list(map(int, self.input.split(',')))

    def part_1(self):
        return self.calculate(12, 2)

    def part_2(self):
        for a in range(100):
            for b in range(100):
                if self.calculate(a, b) == 19690720:
                    return 100 * a + b

    def calculate(self, value1, value2):
        numbers = self.numbers[:]

        numbers[1] = value1
        numbers[2] = value2

        cursor = 0
        while numbers[cursor] != 99:
            a, b, c = numbers[cursor + 1:cursor + 4]
            if numbers[cursor] == 1:
                numbers[c] = numbers[a] + numbers[b]
            elif numbers[cursor] == 2:
                numbers[c] = numbers[a] * numbers[b]

            cursor += 4

        return numbers[0]



Day02(__file__).solve()

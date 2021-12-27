from shared.utils import *


class Day02(Solution):
    def part_1(self):
        for line in self.input_lines():
            repeat, letter, password = line.split()
            r_min, r_max = map(int, repeat.split('-'))
            letter = letter[:-1]

            if r_min <= password.count(letter) <= r_max:
                self.add_result()

    def part_2(self):
        for line in self.input_lines():
            repeat, letter, password = line.split()
            r_first, r_second = map(int, repeat.split('-'))
            letter = letter[:-1]

            if [password[r_first - 1], password[r_second - 1]].count(letter) == 1:
                self.add_result()


Day02(__file__).solve()

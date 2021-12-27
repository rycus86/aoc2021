import re

from shared.utils import *


class Day04(Solution):
    passports: List[str]
    required = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')

    def setup(self):
        self.passports = self.input.split('\n\n')

    def part_1(self):
        for passport in self.passports:
            fields = list(map(lambda e: e.split(':')[0], passport.replace('\n', ' ').split(' ')))
            if all(f in fields for f in self.required):
                self.add_result()

    def part_2(self):
        validation = {
            'byr': lambda v: 1920 <= int(v) <= 2002,
            'iyr': lambda v: 2010 <= int(v) <= 2020,
            'eyr': lambda v: 2020 <= int(v) <= 2030,
            'hgt': self.valid_height,
            'hcl': lambda v: re.match(r'#[a-f0-9]{6}$', v),
            'ecl': lambda v: v in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
            'pid': lambda v: len(v) == 9 and all('0' <= d <= '9' for d in v),
            'cid': lambda v: True
        }

        for passport in self.passports:
            entries = passport.replace('\n', ' ').split(' ')
            fields = list(map(lambda e: e.split(':')[0], entries))

            if not all(f in fields for f in self.required):
                continue

            for entry in entries:
                key, value = entry.split(':', 1)
                if not validation[key](value):
                    break
            else:
                self.add_result()

    def valid_height(self, value):
        if value.endswith('cm'):
            return 150 <= int(value[:-2]) <= 193
        elif value.endswith('in'):
            return 59 <= int(value[:-2]) <= 76


Day04(__file__).solve()

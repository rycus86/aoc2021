import functools
import re

from shared.utils import *


class Record:
    def __init__(self, line: str):
        self.report = line.split(' ')[0]
        self.groups = list(map(int, line.split(' ')[1].split(',')))
        self.glen = len(self.groups)
        self.gsum = sum(self.groups)

    def unfold(self):
        self.report = '?'.join([self.report] * 5)
        self.groups = self.groups * 5
        self.glen = len(self.groups)
        self.gsum = sum(self.groups)

    def count_matches2(self):
        @functools.cache
        def _generate(part: str, groups: Tuple[int]):
            if not groups:
                if '#' not in part:
                    return 1
                else:
                    return 0

            found = 0

            group, rem_groups = groups[0], groups[1:]
            min_rem_len = sum(rem_groups) + len(rem_groups)

            for idx in range(len(part) - min_rem_len - group + 1):
                search, len_search = f'^[.?]{{{idx}}}[#?]{{{group}}}', idx + group
                if len(part) >= len_search + 1:
                    search += '[.?]'
                    len_search += 1

                if re.match(search, part):
                    found += _generate(part[len_search:], rem_groups)

            return found

        return _generate(self.report, tuple(self.groups))

    def count_matches(self):
        return sum(self._generate(self.report))

    def _generate(self, s: str):
        if s.count('#') > self.gsum:
            return

        pos = s.find('?')

        if pos > -1:
            part = s[:pos]
            final = False
        else:
            part = s
            final = True

        if not self._check_ok(part, final):
            return

        if final:
            yield 1

        else:
            rem = s[pos+1:]
            yield sum(self._generate(part + '.' + rem))
            yield sum(self._generate(part + '#' + rem))

    def _check_ok(self, part: str, final=False) -> bool:
        parts = [len(p) for p in part.split('.') if p != '']
        lenp = len(parts)

        if lenp > self.glen:
            return False
        if final and lenp != self.glen:
            return False

        for idx, pl in enumerate(parts):
            if idx >= self.glen:
                return False
            if not final and idx == lenp - 1:
                if pl > self.groups[idx]:
                    return False
            elif pl != self.groups[idx]:
                return False

        return True

    def __repr__(self):
        return f'{self.report} {self.groups}'


class Day12(Solution):
    rows: List[Record]

    def setup(self):
        self.rows = list(map(Record, self.input_lines()))

    def part_1(self):
        for row in self.rows:
            self.add_result(row.count_matches())

    def part_2(self):
        for idx, row in enumerate(self.rows):
            row.unfold()
            self.add_result(row.count_matches2())


Day12(__file__).solve()

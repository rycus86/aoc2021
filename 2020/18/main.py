from shared.utils import *


class Group(object):
    def __init__(self, contents, parse=True):
        self.groups = dict()  # type: Dict[str, Group]

        if not parse:
            self.data = contents

        elif contents[0] != '(':
            self.data = contents

        else:
            self.data = ''
            num_parens = 0

            for c in contents:
                if c == '(':
                    num_parens += 1
                    if num_parens == 1:
                        continue
                elif c == ')':
                    num_parens -= 1
                    if num_parens == 0:
                        break

                self.data += c

        self.extract_groups()

    def extract_groups(self):
        start = None
        num_parens = 0
        for idx, c in enumerate(self.data):
            if c == '(':
                if num_parens == 0:
                    start = idx
                num_parens += 1
            elif c == ')':
                num_parens -= 1
                if num_parens == 0:
                    data = self.data[start:idx+1]
                    self.groups[data] = Group(data)

    def evaluate(self, is_part2=False) -> int:
        formula = self.data
        for key, child in self.groups.items():
            formula = formula.replace(key, str(child.evaluate(is_part2)))

        if is_part2:
            return self._calculate_part2(formula)
        else:
            return self._calculate_part1(formula)

    def _calculate_part1(self, formula: str) -> int:
        parts = formula.split(' ')
        while len(parts) >= 3:
            a, op, b = parts[0:3]
            parts = parts[3:]

            if op == '+':
                result = int(a) + int(b)
            elif op == '*':
                result = int(a) * int(b)
            else:
                raise Exception(f'unexpected operation: {op}')

            parts = [str(result)] + parts

        assert len(parts) == 1, f'remaining parts: {parts}'
        return int(parts[0])

    def _calculate_part2(self, formula: str) -> int:
        parts = formula.split(' ')
        while len(parts) >= 3:
            first_addition = parts.index('+') if '+' in parts else -1
            if first_addition > 1:
                a, op, b = parts[first_addition-1:first_addition+2]
            else:
                a, op, b = parts[0:3]
                parts = parts[3:]

            if op == '+':
                result = int(a) + int(b)
            elif op == '*':
                result = int(a) * int(b)
            else:
                raise Exception(f'unexpected operation: {op}')

            if first_addition > 1:
                parts[first_addition-1:first_addition+2] = [str(result)]
            else:
                parts = [str(result)] + parts

        assert len(parts) == 1, f'remaining parts: {parts}'
        return int(parts[0])

    def __repr__(self):
        printed = self.data
        for key, child in self.groups.items():
            printed = printed.replace(key, f' < {child} > ')
        return printed


class Day18(Solution):

    def part_1(self):
        for line in self.input_lines():
            group = Group(line, parse=False)
            self.add_result(group.evaluate())

    def part_2(self):
        for line in self.input_lines():
            group = Group(line, parse=False)
            self.add_result(group.evaluate(is_part2=True))


Day18(__file__).solve()

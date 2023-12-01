from shared.utils import *


class Test:
    def __init__(self, instruction: str):
        if ':' in instruction:
            condition, self.target = instruction.split(':')
            self.variable, self.op, self.value = condition[0], condition[1], int(condition[2:])
        else:
            self.op = None
            self.target = instruction

    def __repr__(self):
        if self.op:
            return f'{self.variable} {self.op} {self.value} -> {self.target}'
        else:
            return f'=> {self.target}'

    def test(self, xmas: Dict[str, int]):
        if self.op is None:
            return True

        if self.op == '<':
            return xmas[self.variable] < self.value
        elif self.op == '>':
            return xmas[self.variable] > self.value
        else:
            raise ValueError(f'unknown operator: {self.op}')

    def apply_limits(self, xmas: Dict[str, Tuple[int, int]]):
        if self.op is None:
            return dict(xmas), None

        a, b = xmas[self.variable]
        xmas_for_target = dict(xmas)
        xmas_for_following = dict(xmas)

        if self.op == '<':
            mine, other = (a, min(b, self.value - 1)), (self.value, b)
        elif self.op == '>':
            mine, other = (self.value + 1, b), (a, min(b, self.value))
        else:
            raise ValueError(f'unknown operator: {self.op}')

        if mine[0] > mine[1]:
            xmas_for_target = None
        else:
            xmas_for_target[self.variable] = mine

        if other[0] > other[1]:
            xmas_for_following = None
        else:
            xmas_for_following[self.variable] = other

        return xmas_for_target, xmas_for_following


class Day19(Solution):
    instructions: Dict[str, List[Test]]
    parts = List[Dict[str, int]]

    def setup(self):
        self.instructions = dict()
        self.parts = list()

        for line in self.input_lines():
            if not line.strip():
                continue

            if line.startswith('{'):
                items = dict()
                for item in line[1:-1].split(','):
                    key, value = item.split('=')
                    items[key] = int(value)
                self.parts.append(items)
                continue

            key, ins_list = line.replace('}', '').split('{')
            self.instructions[key] = list(map(Test, ins_list.split(',')))

    def part_1(self):
        for part in self.parts:
            instruction = 'in'
            while instruction not in ('R', 'A'):
                for test in self.instructions[instruction]:
                    if test.test(part):
                        instruction = test.target
                        break

            if instruction == 'A':
                self.add_result(sum(part.values()))

    def part_2(self):
        return self.sum_instruction('in', dict(x=(1, 4000), m=(1, 4000), a=(1, 4000), s=(1, 4000)))

    def sum_instruction(self, key: str, xmas: Dict[str, Tuple[int, int]]):
        total = 0

        if key == 'R':
            return 0

        if key == 'A':
            total = 1
            for low, high in xmas.values():
                total *= high - low + 1
            return total

        for test in self.instructions[key]:
            mine, other = test.apply_limits(xmas)

            if mine:
                total += self.sum_instruction(test.target, mine)

            if other:
                xmas = other

        return total


Day19(__file__).solve()

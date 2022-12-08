from shared.utils import *

from typing import Callable


class Monkey(object):

    def __init__(self, index: int, items: List[int], operator: str, operand, test: int, if_true: int, if_false: int):
        self.index = index
        self.items = items
        self.operator = operator
        self.operand = operand
        self.test = test
        self.if_true = if_true
        self.if_false = if_false
        self.inspects = 0


class Day11(Solution):
    monkeys: List[Monkey]

    def setup(self):
        self.monkeys = list()

        current_monkey = None
        current_items = None
        current_operator = None
        current_operand = None
        current_test = None
        current_if_true = None
        current_if_false = None

        for line in self.input_lines():
            if line.startswith('Monkey '):
                current_monkey = int(line.replace(':', '').split()[-1])
            elif 'Starting items: ' in line:
                current_items = list(map(int, line.replace('Starting items:', '').replace(' ', '').split(',')))
            elif 'Operation: new = old ' in line:
                line = line.replace('  Operation: new = old ', '')
                current_operator, current_operand = line.split()
                if current_operand == 'old':
                    current_operand = None
                else:
                    current_operand = int(current_operand)
            elif 'Test: divisible by ' in line:
                current_test = int(line.split()[-1])
            elif 'If true:' in line:
                current_if_true = int(line.split()[-1])
            elif 'If false:' in line:
                current_if_false = int(line.split()[-1])
            elif not line.strip():
                self.monkeys.append(Monkey(current_monkey, current_items,
                                           current_operator, current_operand,
                                           current_test, current_if_true, current_if_false))
        else:
            self.monkeys.append(Monkey(current_monkey, current_items,
                                       current_operator, current_operand,
                                       current_test, current_if_true, current_if_false))

    def part_1(self):
        return self.run_monkey_business(20, part_1=True)

    def part_2(self):
        return self.run_monkey_business(10000, part_1=False)

    def run_monkey_business(self, rounds, part_1):
        reducer = 1
        for monkey in self.monkeys:
            reducer *= monkey.test

        for _ in range(rounds):
            for monkey in self.monkeys:
                monkey.inspects += len(monkey.items)

                while monkey.items:
                    item = monkey.items.pop(0)
                    if monkey.operand is None:
                        if monkey.operator == '+':
                            item = item + item
                        else:
                            item = item * item
                    else:
                        if monkey.operator == '+':
                            item = item + monkey.operand
                        else:
                            item = item * monkey.operand

                    if part_1:
                        item = item // 3
                    else:
                        item = item % reducer

                    if item % monkey.test == 0:
                        target = monkey.if_true
                    else:
                        target = monkey.if_false
                    self.monkeys[target].items.append(item)

        all_inspects = [m.inspects for m in self.monkeys]
        m1, m2 = list(sorted(all_inspects))[-2:]
        return m1 * m2


Day11(__file__).solve()

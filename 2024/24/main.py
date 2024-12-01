from shared.utils import *


class Day24(Solution):
    values: dict[str, bool]

    def setup(self):
        self.values = dict()

        for line in self.input_lines():
            if ':' in line:
                key, value = line.split(':')
                self.values[key] = value.strip() == '1'

    def part_1(self):
        all_rules = [line for line in self.input_lines() if '->' in line]

        while all_rules:
            line = all_rules.pop(0)
            rule, output = line.split(' -> ')
            op1, operator, op2 = rule.split(' ')

            if op1 not in self.values or op2 not in self.values:
                all_rules.append(line)
                continue

            if operator == 'AND':
                self.values[output] = self.values[op1] and self.values[op2]
            elif operator == 'OR':
                self.values[output] = self.values[op1] or self.values[op2]
            elif operator == 'XOR':
                self.values[output] = self.values[op1] ^ self.values[op2]

        number = 0
        for key, value in self.values.items():
            if value and key.startswith('z'):
                index = int(key[1:])
                number += 1 << index

        return number

    class Rule:
        def __init__(self, line):
            rule, self.output = line.split(' -> ')
            self.op1, self.operator, self.op2 = rule.split(' ')

        def is_available(self, values):
            if self.op1 not in values or self.op2 not in values:
                return False
            else:
                return True

        def calculate(self, values):
            if self.operator == 'AND':
                return values[self.op1] and values[self.op2]
            elif self.operator == 'OR':
                return values[self.op1] or values[self.op2]
            elif self.operator == 'XOR':
                return values[self.op1] ^ values[self.op2]

        def is_invalid_z_output(self, rules):
            return self.output != max(r.output for r in rules) and self.output[0] == 'z' and self.operator != 'XOR'

        def is_invalid_xor_rule(self):
            return self.operator == 'XOR' and self.output[0] not in 'xyz' and self.op1[0] not in 'xyz' and self.op2[0] not in 'xyz'

        def is_invalid_and_rule_without_matching_or_rule(self, rules):
            if self.operator == 'AND' and 'x00' not in (self.op1, self.op2):
                return any(r.operator != 'OR' and (self.output == r.op1 or self.output == r.op2) for r in rules)

        def is_invalid_xor_rule_for_internal_wires(self, rules):
            if self.operator == 'XOR':
                return any(r.operator == 'OR' and (self.output == r.op1 or self.output == r.op2) for r in rules)

        def __repr__(self):
            return f'{self.op1} {self.operator} {self.op2} -> {self.output}'

        def __hash__(self):
            return hash((self.op1, self.operator, self.op2, self.output))

    def find_rule_by_output(self, rules, output):
        for rule in rules:
            if rule.output == output:
                return rule

    def find_rule_by_line(self, rules, line):
        for rule in rules:
            if str(line) == line:
                return rule

    def print_failing_rule(self, rules, rule, values, indent, ok_rules=None):
        print(f'{" " * indent * 2}{"%02d" % indent}| {rule.output}: {rule} =>', values[rule.output])
        if ok_rules and rule in ok_rules:
            return
        if rule.op1[0] not in 'xy':
            self.print_failing_rule(rules, self.find_rule_by_output(rules, rule.op1), values, indent + 1, ok_rules)
        if rule.op2[0] not in 'xy':
            self.print_failing_rule(rules, self.find_rule_by_output(rules, rule.op2), values, indent + 1, ok_rules)

    # based on https://www.reddit.com/r/adventofcode/comments/1hl698z/comment/m3kt1je/
    def part_2(self):
        rules = [Day24.Rule(line) for line in self.input_lines() if '->' in line]

        wrong_rules = set()
        for rule in rules:
            if rule.is_invalid_z_output(rules):
                wrong_rules.add(rule)
            elif rule.is_invalid_xor_rule():
                wrong_rules.add(rule)
            elif rule.is_invalid_and_rule_without_matching_or_rule(rules):
                wrong_rules.add(rule)
            elif rule.is_invalid_xor_rule_for_internal_wires(rules):
                wrong_rules.add(rule)

        return ','.join(sorted(map(lambda r: r.output, wrong_rules)))


Day24(__file__).solve()

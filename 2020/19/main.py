import re

from shared.utils import *


class Rule(object):
    key: int
    letter: Optional[str]
    rules: Optional[List[List[int]]]

    def __init__(self, description: str):
        key, rule = description.split(': ')
        self.key = int(key)

        if rule.startswith('"'):
            self.letter = rule.replace('"', '')
            self.rules = None
        else:
            self.letter = None
            self.rules = list()
            for part in rule.split(' | '):
                self.rules.append(list(map(int, part.split(' '))))

    def __repr__(self):
        return f'Rule[{self.key}]: {self.letter or self.rules}'


class Day19(Solution):
    rules: Dict[int, Rule]
    messages: List[str]
    pattern: re.Pattern
    re_overrides: Dict[int, str]

    def setup(self):
        in_rules, in_messages = self.input.split('\n\n')

        self.rules = dict()
        for rule in in_rules.splitlines():
            parsed = Rule(rule)
            self.rules[parsed.key] = parsed

        self.messages = in_messages.splitlines()
        self.re_overrides = None

    def to_regex(self, rule):
        if self.re_overrides and rule.key in self.re_overrides:
            return self.re_overrides[rule.key]

        if rule.letter:
            return rule.letter

        converted_rules = list()
        for rules in rule.rules:
            converted_rules.append(''.join(self.to_regex(self.rules[child]) for child in rules))

        return '(?:' + '|'.join(converted_rules) + ')'

    def part_1(self):
        self.pattern = re.compile(f'^{self.to_regex(self.rules[0])}$')

        for message in self.messages:
            if self.pattern.match(message):
                self.add_result()

    def part_2(self):
        rule_11_inner = lambda r: f'{self._to_re(42)}{{{r}}}{self._to_re(31)}{{{r}}}'

        self.re_overrides = {
            # 8: 42 | 42 8  --  repeat one or more times
            8: f'(?:{self._to_re(42)}+)',
            # 11: 42 31 | 42 11 31  -- repeat both the left and right sides the same amount of times (max 10)
            11: f'(?:{"|".join(rule_11_inner(r) for r in range(1, 10))})'
        }

        self.pattern = re.compile(f'^{self.to_regex(self.rules[0])}$')

        for message in self.messages:
            if self.pattern.match(message):
                self.add_result()

    def _to_re(self, rule_index: int) -> str:
        return self.to_regex(self.rules[rule_index])


Day19(__file__).solve()

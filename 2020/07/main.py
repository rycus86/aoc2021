from collections import defaultdict

from shared.utils import *


class Day07(Solution):
    rules: Dict[str, List[Tuple[str, int]]]
    reverse_rules: Dict[str, Set[str]]

    def setup(self):
        self.rules = defaultdict(list)
        self.reverse_rules = defaultdict(set)

        for rule in self.input_lines():
            container, contains = rule.split(' bags contain ')
            for target in contains.strip('.').split(', '):
                target = target.split(' bag')[0]

                if target == 'no other':
                    self.rules[container] = list()
                else:
                    count, kind = target.split(' ', 1)
                    count = int(count)

                    self.rules[container].append((kind, count))
                    self.reverse_rules[kind].add(container)

    def part_1(self):
        total = set()
        to_check = self.reverse_rules['shiny gold']
        while to_check:
            check = to_check.pop()
            if check in total:
                continue
            else:
                total.add(check)
                to_check.update(self.reverse_rules[check])

        return len(total)

    def part_2(self):
        to_add = [(1, 'shiny gold')]
        while to_add:
            count, kind = to_add.pop(0)
            for child, child_count in self.rules[kind]:
                self.add_result(count * child_count)
                to_add.append((count * child_count, child))


Day07(__file__).solve()

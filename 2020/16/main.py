from shared.utils import *


class Day16(Solution):
    rules: Dict[str, List[Tuple[int, int]]]
    valid_values: Dict[int, bool]
    my_ticket: List[int]
    nearby_tickets: List[List[int]]
    valid_other_tickets: List[List[int]] = list()

    def setup(self):
        self.rules = dict()
        self.valid_values = {i: False for i in range(1000)}
        self.nearby_tickets = list()

        sections = self.input.split('\n\n')

        for line in sections[0].splitlines():
            key, entries = line.split(': ')
            self.rules[key] = list()

            for ranges in entries.split(' or '):
                start, end = map(int, ranges.split('-'))
                self.rules[key].append((start, end))
                self.valid_values.update({i: True for i in range(start, end + 1)})

        self.my_ticket = list(map(int, sections[1].splitlines()[1].split(',')))

        for line in sections[2].splitlines()[1:]:
            self.nearby_tickets.append(list(map(int, line.split(','))))

    def part_1(self):
        for ticket in self.nearby_tickets:
            valid = True

            for value in ticket:
                if not self.valid_values[value]:
                    self.add_result(value)
                    valid = False

            if valid:
                self.valid_other_tickets.append(ticket)

    def part_2(self):
        ticket_values = {idx: set() for idx in range(len(self.my_ticket))}

        for ticket in self.valid_other_tickets:
            for idx, value in enumerate(ticket):
                ticket_values[idx].add(value)

        targets = {key: set() for key in self.rules}

        for key, ranges in self.rules.items():
            for idx, values in ticket_values.items():
                possible = True
                for value in values:
                    if not any(start <= value <= end for start, end in ranges):
                        possible = False
                        break

                if possible:
                    targets[key].add(idx)

        mapping = dict()  # type: Dict[str, int]

        choices = list((len(indexes), key, indexes) for key, indexes in targets.items())
        for _, key, indexes in sorted(choices):
            for idx in indexes:
                if idx not in mapping.values():
                    mapping[key] = idx
                    break

        result = 1

        for key, idx in mapping.items():
            if key.startswith('departure'):
                result *= self.my_ticket[idx]

        return result


Day16(__file__).solve()

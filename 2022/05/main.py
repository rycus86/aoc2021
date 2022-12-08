from shared.utils import *


class Day05(Solution):
    stacks: List[List[str]]

    def setup(self):
        for line in self.input_lines():
            if not all(ch in '123456789 ' for ch in line):
                continue

            num = int(line.replace(' ', '')[-1])
            break
        else:
            raise Exception('That did not work')

        self.stacks = list()
        for _ in range(num):
            self.stacks.append(list())

        for line in self.input_lines():
            if '[' not in line:
                break

            for pos in range(1, 1 + 4 * num, 4):
                if pos < len(line) and line[pos] != ' ':
                    self.stacks[pos // 4].append(line[pos])

    def part_1(self):
        return self.rearrange(reversing=True)

    def part_2(self):
        return self.rearrange(reversing=False)

    def rearrange(self, reversing):
        for line in self.input_lines():
            if not line.startswith('move '):
                continue

            _, count, _, source, _, dest = line.split()
            count, source, dest = int(count), int(source) - 1, int(dest) - 1

            moving, self.stacks[source] = self.stacks[source][0:count], self.stacks[source][count:]
            if reversing:
                moving = list(reversed(moving))
            self.stacks[dest] = moving + self.stacks[dest]

        return ''.join(s[0] for s in self.stacks)


Day05(__file__).solve()

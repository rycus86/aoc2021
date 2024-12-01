from shared.utils import *


class Day22(Solution):

    def next_secret(self, v: int):
        v = ((v * 64) ^ v) % 16777216
        v = ((v // 32) ^ v) % 16777216
        return ((v * 2048) ^ v) % 16777216

    def part_1(self):
        for line in self.input_lines():
            value = int(line)
            for _ in range(2000):
                value = self.next_secret(value)
            self.add_result(value)

    def part_2(self):
        all_prices = defaultdict(int)
        for line in self.input_lines():
            value = int(line)
            prices = dict()
            previous = None
            sequence = list()
            for _ in range(2000):
                value = self.next_secret(value)
                price = value % 10
                if previous is not None:
                    sequence.append(price - previous)
                    if len(sequence) == 4:
                        key = tuple(sequence)
                        if key not in prices:
                            prices[key] = price
                        sequence.pop(0)
                previous = price

            for key, price in prices.items():
                all_prices[key] += price

        return max(all_prices.values())


Day22(__file__).solve()

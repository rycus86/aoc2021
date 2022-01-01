from shared.utils import *


class Day08(Solution):
    layers: List[str]

    def setup(self):
        self.layers = list()

        page_size = 25 * 6

        input_remaining = self.input
        while input_remaining:
            self.layers.append(input_remaining[:page_size])
            input_remaining = input_remaining[page_size:]

    def part_1(self):
        min_zeroes = 10 ** 12
        result = None

        for layer in self.layers:
            if layer.count('0') < min_zeroes:
                result = layer.count('1') * layer.count('2')
                min_zeroes = layer.count('0')

        return result

    def part_2(self):
        image = list()
        for _ in range(6):
            image.append([2] * 25)

        for layer in self.layers:
            for row in range(6):
                for column in range(25):
                    if image[row][column] != 2:
                        continue
                    else:
                        image[row][column] = int(layer[row * 25 + column])

        for row in image:
            for column in row:
                if column == 0:
                    print(' ', end='')
                elif column == 1:
                    print('#', end='')
            print()


Day08(__file__).solve()

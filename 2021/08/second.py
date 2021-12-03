
def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


class Mappings(object):
    def __init__(self):
        self.data = dict()
        self._sort_cache = dict()

    def sorted_string(self, key):
        if key not in self._sort_cache:
            self._sort_cache[key] = ''.join(sorted(key))

        return self._sort_cache[key]

    def is_known(self, pattern):
        return any(key == self.sorted_string(pattern) for key in self.data.values())

    def add_pattern(self, pattern, digit):
        self.data[digit] = self.sorted_string(pattern)

    def is_digit_known(self, digit):
        return digit in self.data

    def pattern_has_segments_of_digit(self, pattern, digit):
        return digit in self.data and all(p in pattern for p in self.data[digit])

    def digit_has_segments_of_pattern(self, pattern, digit):
        return digit in self.data and all(p in self.data[digit] for p in pattern)

    def is_complete(self):
        return len(self.data) == 10

    def translate(self, pattern):
        for digit, value in self.data.items():
            if value == self.sorted_string(pattern):
                return str(digit)


if __name__ == '__main__':
    digits = {
        0: 'abcefg',
        1: 'cf',
        2: 'acdeg',
        3: 'acdfg',
        4: 'bcdf',
        5: 'abdfg',
        6: 'abdefg',
        7: 'acf',
        8: 'abcdefg',
        9: 'abcdfg'
    }

    total = 0

    for line in read_input().splitlines(keepends=False):
        signal_patterns, output_values = line.split(' | ')

        mappings = Mappings()

        for pattern in signal_patterns.split(' '):
            for d in (1, 4, 7, 8):
                if len(pattern) == len(digits[d]):
                    mappings.add_pattern(pattern, d)

        while not mappings.is_complete():
            for pattern in signal_patterns.split(' '):
                if not mappings.is_known(pattern):

                    if len(pattern) == 5:  # can be 2 3 5
                        if mappings.pattern_has_segments_of_digit(pattern, 1):
                            mappings.add_pattern(pattern, 3)  # 3 has all the segments of 1

                        elif mappings.digit_has_segments_of_pattern(pattern, 6):
                            mappings.add_pattern(pattern, 5)  # 5's segments are all in 6 too

                        elif mappings.is_digit_known(3) and mappings.is_digit_known(5):
                            mappings.add_pattern(pattern, 2)  # only 2 is left unknown at this point

                    elif len(pattern) == 6:  # can be 0 6 9
                        if not mappings.pattern_has_segments_of_digit(pattern, 1):
                            mappings.add_pattern(pattern, 6)  # only 6 does not have all the segments as 1

                        elif mappings.pattern_has_segments_of_digit(pattern, 5):
                            mappings.add_pattern(pattern, 9)    # 9 has all the segments as 5

                        elif mappings.is_digit_known(6) and mappings.is_digit_known(9):
                            mappings.add_pattern(pattern, 0)  # only 0 is left unknown at this point

        output = int(''.join(mappings.translate(pattern) for pattern in output_values.split(' ')))
        # print('output:', output)

        total += output

    print('result:', total)

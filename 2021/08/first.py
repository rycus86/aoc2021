
def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


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
    by_lengths = {
        len(digits[d]): d for d in digits
    }

    total = 0

    for line in read_input().splitlines(keepends=False):
        signal_patterns, output_values = line.split(' | ')

        for pattern in output_values.split(' '):
            if by_lengths[len(pattern)] in (1, 4, 7, 8):
                total += 1

    print('result:', total)

def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


if __name__ == '__main__':
    from collections import defaultdict
    zeroes, ones = defaultdict(lambda: 0), defaultdict(lambda: 0)

    line = ''
    for line in read_input().splitlines():
        for idx, bit in enumerate(line):
            if bit == '0':
                zeroes[idx] += 1
            elif bit == '1':
                ones[idx] += 1

    gamma, epsilon = '', ''
    for idx in range(len(line)):
        if zeroes[idx] > ones[idx]:
            gamma += '0'
            epsilon += '1'
        else:
            gamma += '1'
            epsilon += '0'

    gamma, epsilon = int(gamma, 2), int(epsilon, 2)

    print(f'gamma={gamma} epsilon={epsilon} result={gamma*epsilon}')

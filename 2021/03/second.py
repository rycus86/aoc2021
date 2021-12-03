def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


if __name__ == '__main__':
    from collections import defaultdict
    zeroes, ones = defaultdict(lambda: 0), defaultdict(lambda: 0)

    all_items = read_input().splitlines()

    oxygen = all_items[:]
    for idx in range(len(all_items[0])):
        ones = [item for item in oxygen if item[idx] == '1']
        zeroes = [item for item in oxygen if item[idx] == '0']

        if len(ones) >= len(zeroes):
            oxygen = ones
        else:
            oxygen = zeroes

        # print(f'o={oxygen}')
        if len(oxygen) == 1:
            break

    co2 = all_items[:]
    for idx in range(len(all_items[0])):
        ones = [item for item in co2 if item[idx] == '1']
        zeroes = [item for item in co2 if item[idx] == '0']

        if len(ones) < len(zeroes):
            co2 = ones
        else:
            co2 = zeroes

        # print(f'co2={co2}')
        if len(co2) == 1:
            break

    oxygen, co2 = int(oxygen[0], 2), int(co2[0], 2)
    print(f'o={oxygen} co2={co2} result= {oxygen*co2}')

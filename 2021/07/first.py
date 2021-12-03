
def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


if __name__ == '__main__':
    positions = list(map(int, read_input().split(',')))
    min_pos, max_pos = min(*positions), max(*positions)

    min_cost = None

    for target in range(min_pos, max_pos+1):
        total = 0
        for pos in positions:
            total += abs(target - pos)

        if min_cost is None or min_cost > total:
            min_cost = total
            print(f'cost at {target} is {total}')

        # print(f'cost at {target} is {total}')

    print('result:', min_cost)

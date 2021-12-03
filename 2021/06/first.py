
def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


if __name__ == '__main__':
    ages = list(map(int, read_input().split(',')))

    # print('init', ages)

    for day in range(80):
        new_ages = []
        extras = []
        for age in ages:
            if age == 0:
                extras.append(8)
                new_ages.append(6)
            else:
                new_ages.append(age - 1)

        new_ages.extend(extras)
        ages = new_ages

        # print(f'day {day+1}:', ages)

    print('result:', len(ages))

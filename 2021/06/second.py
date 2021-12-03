
def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


if __name__ == '__main__':
    ages = list(map(int, read_input().split(',')))

    fishes_at_age = {
        age: ages.count(age) for age in range(9)
    }

    # print('init', fishes_at_age)

    for day in range(256):
        new_fishes = fishes_at_age[0]

        for age in range(8):
            fishes_at_age[age] = fishes_at_age[age+1]

        fishes_at_age[8] = new_fishes
        fishes_at_age[6] += new_fishes

        # print(f'day {day+1}:', fishes_at_age, 'new:', new_fishes)

    print('result:', sum(fishes_at_age.values()))

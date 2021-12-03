def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


def roll_value(idx):
    base = 1 + idx * 3
    if base > 100:
        base = base % 100

    v2, v3 = base + 1, base + 2
    if v2 > 100:
        v2 = v2 % 100
    if v3 > 100:
        v3 = v3 % 100

    # print('roll', base, v2, v3)
    return base + v2 + v3


if __name__ == '__main__':
    s1, s2 = None, None
    for line in read_input().splitlines():
        value = int(line.split(' ')[-1])
        if s1 is None:
            s1 = value
        else:
            s2 = value

    p1 = True
    score_1 = 0
    score_2 = 0
    idx = 0

    while score_1 < 1000 and score_2 < 1000:
        roll = roll_value(idx)
        idx += 1

        if p1:
            s1 += roll
            s1 = s1 % 10
            if s1 == 0:
                s1 = 10
            score_1 += s1
            # print('p1 moved to', s1, 'score:', score_1)
            p1 = False
        else:
            s2 += roll
            s2 = s2 % 10
            if s2 == 0:
                s2 = 10
            score_2 += s2
            # print('p2 moved to', s2, 'score:', score_2)
            p1 = True

        if score_1 >= 1000:
            print(f'result: {score_2}*{idx * 3}', score_2 * idx * 3)
            break
        elif score_2 >= 1000:
            print(f'result: {score_1}*{idx * 3}', score_1 * idx * 3)
            break

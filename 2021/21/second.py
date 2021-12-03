from collections import defaultdict


def compute_possible_rounds():
    values = defaultdict(lambda: 0)

    for x in range(1, 4):
        for y in range(1, 4):
            for z in range(1, 4):
                values[x+y+z] += 1

    return values


possible_rounds = compute_possible_rounds()


def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


def dirac2(val1, val2, pos1, pos2, p1_next: bool, to_add: int, win1: list, win2: list):
    if val1 >= 21:
        win1[0] += to_add
        return
    if val2 >= 21:
        win2[0] += to_add
        return

    for add, count in possible_rounds.items():
        pos = pos1 if p1_next else pos2
        target = (pos + add) % 10
        if target == 0:
            target = 10

        if p1_next:
            dirac2(val1+target, val2, target, pos2, False, to_add * count, win1, win2)
        else:
            dirac2(val1, val2+target, pos1, target, True, to_add * count, win1, win2)


if __name__ == '__main__':
    s1, s2 = None, None
    for line in read_input().splitlines():
        value = int(line.split(' ')[-1])
        if s1 is None:
            s1 = value
        else:
            s2 = value

    win1, win2 = [0], [0]
    dirac2(0, 0, s1, s2, True, 1, win1, win2)
    w1, w2 = win1[0], win2[0]

    print('wins #1:', w1)
    print('wins #2:', w2)
    print('result:', max(w1, w2))

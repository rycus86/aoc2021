from collections import defaultdict


def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


if __name__ == '__main__':
    lines = read_input().splitlines(keepends=False)

    template = lines[0]
    rules = dict()

    for line in lines[2:]:
        left, right = line.split(' -> ')
        rules[left] = right

    pairs = defaultdict(int)

    for x in range(len(template) - 1):
        part = template[x:x + 2]
        pairs[part] += 1

    # print('pairs:', pairs)
    counts = defaultdict(int, **{x: template.count(x) for x in set(template)})
    # print('counts:', counts)

    for idx in range(40):
        new_pairs = defaultdict(int)
        for part, amount in pairs.items():
            if part in rules:
                new_l, new_r = part[0] + rules[part], rules[part] + part[1]
                new_pairs[new_l] += amount
                new_pairs[new_r] += amount
                counts[rules[part]] += amount
        pairs = new_pairs

        # print(f'step {idx+1}:', pairs)
        # print('counts:', counts)

    r_max, r_min = max(counts.values()), min(counts.values())
    print(f'result: {r_max} - {r_min} = {r_max - r_min}')

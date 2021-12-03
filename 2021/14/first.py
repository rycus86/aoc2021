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

    # print('Template:', template)
    for idx in range(10):
        replaced = ''
        for x in range(len(template) - 1):
            part = template[x:x + 2]
            if part in rules:
                replaced += template[x]
                replaced += rules[part]
        replaced += template[-1]
        template = replaced

        # print(f'Step {idx+1}: {template}')

    r_max, r_min = 0, len(template)
    for ch in set(template):
        r_max = max(r_max, template.count(ch))
        r_min = min(r_min, template.count(ch))
    print(f'result: {r_max} - {r_min} = {r_max - r_min}')

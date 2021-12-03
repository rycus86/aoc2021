def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


def process_fold(points: list, folding: tuple) -> list:
    result = list()
    direction, position = folding

    for x, y in points:
        tx, ty = x, y

        if direction == 'y':
            if y > position:
                tx, ty = x, 2 * position - y

        else:
            if x > position:
                tx, ty = 2 * position - x, y


        if (tx, ty) not in result:
            result.append((tx, ty))

    return result


if __name__ == '__main__':
    points = list()
    folds = list()

    for line in read_input().splitlines(keepends=False):
        if line.startswith('fold along '):
            details = line[len('fold along '):]
            direction, position = details.split('=')
            folds.append((direction, int(position)))
        elif line.strip():
            points.append(tuple(map(int, line.split(','))))

    # print('points:', points, 'len:', len(points))
    # print('folds:', folds)

    folded = process_fold(points, folds[0])

    # print('points:', folded, 'len:', len(folded))
    print('result:', len(folded))

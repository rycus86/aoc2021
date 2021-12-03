
def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


if __name__ == '__main__':
    size = 1000
    matrix = [0] * size*size
    lines = []

    for line in read_input().splitlines():
        pairs = line.split(' -> ')
        x1, y1 = map(int, pairs[0].split(','))
        x2, y2 = map(int, pairs[1].split(','))

        if x1 == x2 or y1 == y2:
            for x in range(min(x1, x2), max(x1, x2)+1):
                for y in range(min(y1, y2), max(y1, y2)+1):
                    matrix[y*size + x] += 1

        elif abs(x2-x1) == abs(y2-y1):
            x, y = x1, y1
            x_dir = 1 if x1 < x2 else -1
            y_dir = 1 if y1 < y2 else -1

            matrix[y*size + x] += 1
            while x != x2:
                x += x_dir
                y += y_dir
                matrix[y*size + x] += 1

    # for row in range(size):
    #     print(''.join(map(str, matrix[row*size:row*size+size])).replace('0', '.'))

    result = size*size - matrix.count(0) - matrix.count(1)
    print('result:', result)

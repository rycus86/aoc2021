def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


def extend_image(image, round):
    w = len(image[0])
    pad = 2
    padding = '#' if round % 2 == 1 else '.'
    pad_row = padding * (w + pad * 2)

    new_image = list()
    for _ in range(pad):
        new_image.append(pad_row)

    for row in image:
        new_image.append(padding * pad + row + padding * pad)

    for _ in range(pad):
        new_image.append(pad_row)

    return new_image


def enhance_image(image, algorithm, round):
    h, w = len(image), len(image[0])
    new_image = list()
    padding = '#' if round % 2 == 1 else '.'
    new_image.append(padding * (w + 2))
    new_image.append(padding * (w + 2))

    for y in range(1, h-1):
        new_row = padding * 2

        for x in range(1, w-1):
            data = ''
            for dy in range(-1, 2):
                data += ''.join(image[y+dy][x+dx] for dx in range(-1, 2))
            value = int(data.replace('.', '0').replace('#', '1'), 2)
            replacement = algorithm[value]
            new_row += replacement

        new_row += padding * 2
        new_image.append(new_row)

    new_image.append(padding * (w + 2))
    new_image.append(padding * (w + 2))

    return new_image


if __name__ == '__main__':
    algorithm = ''
    image = list()
    start_image = False

    for line in read_input().splitlines():
        if not line.strip():
            start_image = True
        elif start_image:
            image.append(line)
        else:
            algorithm += line

    for idx in range(50):
        image = extend_image(image, idx)
        image = enhance_image(image, algorithm, idx+1)

    print('result:', sum(row.count('#') for row in image))

def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


def test_setting(x1, x2, y1, y2, dx, dy):
    x, y = 0, 0
    max_y = 0

    while x <= x2 and y >= y1:
        x += dx
        y += dy
        max_y = max(y, max_y)

        dy -= 1
        if dx > 0:
            dx -= 1
        elif dx < 0:
            dx += 1

        if x1 <= x <= x2 and y1 <= y <= y2:
            return True, max_y, x, y

    return False, max_y, x, y


if __name__ == '__main__':
    import re

    input_pattern = re.compile(r'target area: x=([0-9-]+)\.\.([0-9-]+), y=([0-9-]+)\.\.([0-9-]+)')
    x1, x2, y1, y2 = map(int, input_pattern.match(read_input()).groups())

    # print('7,2:', test_setting(x1, x2, y1, y2, 7, 2))
    # print('6,3:', test_setting(x1, x2, y1, y2, 6, 3))
    # print('9,0:', test_setting(x1, x2, y1, y2, 9, 0))
    # print('17,-4:', test_setting(x1, x2, y1, y2, 17, -4))
    # print('6,9:', test_setting(x1, x2, y1, y2, 6, 9))

    dxl = list()
    for i in range(1, x1):
        tx = i * (i + 1) / 2
        if x1 <= tx <= x2:
            dxl.append(i)
    print(f'dx={dxl}')

    max_y = 0
    for dx in dxl:
        for dy in range(100):
            success, my, x, y = test_setting(x1, x2, y1, y2, dx, dy)
            if success:
                print(f'Found: {x},{y} => {my}')
                max_y = max(my, max_y)

    print('result:', max_y)

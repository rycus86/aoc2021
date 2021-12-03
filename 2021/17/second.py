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

        if x1 <= x <= x2 and y1 <= y <= y2:
            return True, max_y, x, y

    return False, max_y, x, y


if __name__ == '__main__':
    import re

    input_pattern = re.compile(r'target area: x=([0-9-]+)\.\.([0-9-]+), y=([0-9-]+)\.\.([0-9-]+)')
    x1, x2, y1, y2 = map(int, input_pattern.match(read_input()).groups())

    dxl = set()
    for i in range(x2, 1, -1):
        ix, dx = 0, i
        while ix <= x2:
            ix, dx = ix + dx, max(0, dx - 1)
            if x1 <= ix <= x2:
                dxl.add(i)
            if dx == 0:
                break

    solutions = set()
    for dx in dxl:
        for dy in range(y1, 100):
            success, my, x, y = test_setting(x1, x2, y1, y2, dx, dy)
            if success:
                solutions.add((dx, dy))

    print('result:', len(solutions))

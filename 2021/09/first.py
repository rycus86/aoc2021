
def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


if __name__ == '__main__':
    area = list(map(list, read_input().splitlines(keepends=False)))

    w, h = len(area[0]), len(area)
    risk = 0

    for y in range(h):
        for x in range(w):
            loc = area[y][x]
            above = y == 0 or area[y-1][x] > loc
            below = y == h - 1 or area[y+1][x] > loc
            left = x == 0 or area[y][x-1] > loc
            right = x == w - 1 or area[y][x+1] > loc

            if above and below and left and right:
                risk += int(loc) + 1

    print('result:', risk)

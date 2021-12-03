
def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


if __name__ == '__main__':
    area = list(map(list, read_input().splitlines(keepends=False)))

    w, h = len(area[0]), len(area)
    low_points = list()

    for y in range(h):
        for x in range(w):
            loc = area[y][x]
            above = y == 0 or area[y-1][x] > loc
            below = y == h - 1 or area[y+1][x] > loc
            left = x == 0 or area[y][x-1] > loc
            right = x == w - 1 or area[y][x+1] > loc

            if above and below and left and right:
                low_points.append((x, y))

    basin_sizes = list()

    for lx, ly in low_points:
        basin = [(lx, ly)]
        previous_size = 0

        while len(basin) > previous_size:
            previous_size = len(basin)

            for bx, by in basin:
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    x, y = bx+dx, by+dy
                    if (x, y) in basin:
                        continue
                    if x < 0 or y < 0 or x >= w or y >= h:
                        continue

                    if area[y][x] == '9':
                        continue

                    basin.append((x, y))

        basin_sizes.append(len(basin))

    result = 1
    for size in list(reversed(sorted(basin_sizes)))[0:3]:
        result *= size

    print('result:', result)

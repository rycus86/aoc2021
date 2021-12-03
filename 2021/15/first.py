def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


if __name__ == '__main__':
    grid = list()

    for line in read_input().splitlines(keepends=False):
        grid.append(list(map(int, line)))

    w, h = len(grid[0]), len(grid)

    risk = [10 ** 100] * w * h
    risk[0] = 0

    for y in range(h):
        for x in range(w):
            cr = risk[w * y + x]

            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                tx, ty = x + dx, y + dy
                if tx < 0 or ty < 0 or tx >= w or ty >= h:
                    continue

                tg = grid[ty][tx]
                tr = risk[w * ty + tx]

                if tr > cr + tg:
                    risk[w * ty + tx] = cr + tg

    # for y in range(h):
    #     for x in range(w):
    #         print('%3d' % risk[w*y+x], end=' ')
    #     print()

    print('result:', risk[-1])

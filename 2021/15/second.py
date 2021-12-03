def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


if __name__ == '__main__':
    grid = list()

    for line in read_input().splitlines(keepends=False):
        row = list(map(int, line))
        rlen = len(row)

        for _ in range(4):
            row += [x + 1 if x < 9 else 1 for x in row[-rlen:]]

        grid.append(row)

    hlen = len(grid)
    for _ in range(4):
        for row in list(grid[-hlen:]):
            grid.append([x + 1 if x < 9 else 1 for x in row])

    # for row in grid:
    #     print(''.join(map(str, row)))

    w, h = len(grid[0]), len(grid)

    risk = [10 ** 100] * w * h
    risk[0] = 0

    needs_recompute = True
    rounds = 0

    while needs_recompute:
        rounds += 1
        needs_recompute = False

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
                        if tx == w - 1 and ty == h - 1:
                            needs_recompute = True

    # print(f'done in {rounds} rounds')
    # for y in range(h):
    #     for x in range(w):
    #         print('%4d' % risk[w*y+x], end=' ')
    #     print()

    print('result:', risk[-1])

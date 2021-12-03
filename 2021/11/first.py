
def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


def increase_all_by_one(grid):
    for idx, row in enumerate(grid):
        grid[idx] = [x+1 for x in row]


def increase_by_one(grid, w, h, x, y):
    if x < 0 or y < 0 or x >= w or y >= h:
        return

    grid[y][x] += 1


def zero_flashed_cells(grid):
    for idx, row in enumerate(grid):
        grid[idx] = [0 if x > 9 else x for x in row]


def flash_all(grid):
    already_flashed = set()
    w, h = len(grid[0]), len(grid)

    previously_flashed = -1

    while len(already_flashed) > previously_flashed:
        previously_flashed = len(already_flashed)

        for y in range(h):
            for x in range(w):

                if grid[y][x] > 9:
                    if (x, y) not in already_flashed:
                        already_flashed.add((x, y))

                        for dx in (-1, 0, 1):
                            for dy in (-1, 0, 1):
                                if not (dx == 0 and dy ==0):
                                    increase_by_one(grid, w, h, x+dx, y+dy)

    zero_flashed_cells(grid)

    return len(already_flashed)


def print_grid(grid):
    for row in grid:
        print(''.join(str(x) for x in row))
    print()


if __name__ == '__main__':
    grid = []

    for line in read_input().splitlines(keepends=False):
        grid.append([int(x) for x in line])

    # print_grid(grid)

    result = 0

    for _ in range(100):
        increase_all_by_one(grid)
        result += flash_all(grid)
        # print_grid(grid)

    print('result:', result)

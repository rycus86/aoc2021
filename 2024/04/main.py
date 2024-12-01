from shared.utils import *


class Day04(Solution):
    grid: Grid

    def setup(self):
        self.grid = self.input_grid()

    def part_1(self):
        grid = self.grid
        for _ in range(4):
            self.add_result(len(list(grid.locate_all('XMAS'))))

            for ri, row in enumerate(grid.rows[:-3]):
                for ci, cell in enumerate(row[:-3]):
                    if cell == 'X':
                        diagonal = 'X'
                        for i in range(1, 4):
                            diagonal += grid.rows[ri + i][ci + i]
                        if diagonal == 'XMAS':
                            self.add_result(1)

            grid = grid.rotate_right(joining='')

    def part_2(self):
        patterns_diag = (
            ((-1, -1), (1, 1)),
            ((1, -1), (-1, 1))
        )

        for x in range(1, self.grid.width - 1):
            for y in range(1, self.grid.height - 1):
                if self.grid.get(x, y) == 'A':
                    group = self.grid.nearby_cells(x, y, include_diagonals=True)
                    if all(''.join(group[(x + dx, y + dy)] for dx, dy in pattern) in ('MS', 'SM') for pattern in patterns_diag):
                        self.add_result(1)


Day04(__file__).solve()

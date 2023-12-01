from shared.utils import *


class Day03(Solution):
    grid: Grid
    all_symbols: Set[str]
    symbol_positions: Set[Tuple[int]]

    def setup(self):
        self.grid = self.input_grid()
        self.all_symbols = set(ch for ch in self.grid.to_string()) - set(ch for ch in '01234567890.\n')
        self.symbol_positions = set(pos for symbol in self.all_symbols for pos in self.grid.locate_all(symbol))

    def part_1(self):
        current_num = ''
        is_adjacent = False

        for y, row in enumerate(self.grid.rows):
            for x, p in enumerate(row):
                if '0' <= p <= '9':
                    current_num += p
                    is_adjacent |= any(pos in self.symbol_positions for pos in self.grid.nearby_cells(x, y, include_diagonals=True).keys())
                else:
                    value, current_num = current_num, ''
                    if value and is_adjacent:
                        self.add_result(int(value))
                    is_adjacent = False

            else:
                value, current_num = current_num, ''
                if value and is_adjacent:
                    self.add_result(int(value))
                is_adjacent = False

    def part_2(self):
        current_num = ''
        is_adjacent = False
        closest_star = None

        parts_to_gears = defaultdict(list)

        for y, row in enumerate(self.grid.rows):
            for x, p in enumerate(row):
                if '0' <= p <= '9':
                    current_num += p
                    for (nx, ny), nc in self.grid.nearby_cells(x, y, include_diagonals=True).items():
                        if nc == '*':
                            is_adjacent = True
                            closest_star = (nx, ny)
                else:
                    value, current_num = current_num, ''
                    if value and is_adjacent:
                        parts_to_gears[closest_star].append(int(value))
                    is_adjacent = False

            else:
                value, current_num = current_num, ''
                if value and is_adjacent:
                    parts_to_gears[closest_star].append(int(value))
                is_adjacent = False

        for parts in parts_to_gears.values():
            if len(parts) == 2:
                self.add_result(var_mul(*parts))


Day03(__file__).solve()

from shared.utils import *


class Day25(Solution):
    keys: list[tuple[int]]
    locks: list[tuple[int]]
    width: int
    height: int

    def setup(self):
        self.keys = list()
        self.locks = list()

        for item in self.input.split('\n\n'):
            grid = Grid(item.splitlines(keepends=False))
            self.width = grid.width
            self.height = grid.height - 1
            heights = tuple(grid.get_column(x).count('#') - 1 for x in range(grid.width))
            if item[0] == '#':  # key
                self.keys.append(heights)
            else:  # lock
                self.locks.append(heights)

    def part_1(self):
        for key in self.keys:
            for lock in self.locks:
                for x in range(self.width):
                    if key[x] + lock[x] >= self.height:
                        break  # bad combination
                else:
                    self.add_result()  # this is ok

    def part_2(self):
        pass


Day25(__file__).solve()

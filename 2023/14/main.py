from shared.utils import *


class Day14(Solution):
    grid: Grid

    def setup(self):
        self.grid = self.input_grid()

    def part_1(self):
        self._roll_north()

        for _, y in self.grid.locate_all('O'):
            self.add_result(self.grid.height - y)

    def part_2(self):
        indexes = dict()
        results = dict()

        for idx in range(1000000000):

            start_hash = hash(self.grid)
            if start_hash not in indexes:
                indexes[start_hash] = idx

            else:
                cycle_length = idx - indexes[start_hash]

                target_idx = idx - 1
                while (1000000000 - 1 - target_idx) % cycle_length != 0:
                    target_idx -= 1

                return results[target_idx]

            for _ in range(4):
                self._roll_north()
                self.grid = self.grid.rotate_right(joining='')

            results[idx] = sum(self.grid.height - y for _, y in self.grid.locate_all('O'))

    def _roll_north(self):
        for x, y in self.grid.locate_all('O'):
            ty = y - 1
            while ty >= 0 and self.grid.get(x, ty) == '.':
                ty -= 1
            if self.grid.get(x, ty + 1) == '.':
                self.grid.set(x, ty + 1, 'O')
                self.grid.set(x, y, '.')


Day14(__file__).solve()

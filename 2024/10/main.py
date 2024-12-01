from shared.utils import *


class Day10(Solution):
    grid: Grid

    def setup(self):
        self.grid = self.input_grid()

    def _walk(self, x: int, y: int,
              found: set[tuple[int, int]],
              path_so_far: tuple[any] = None,
              found_paths: set[any] = None) -> None:

        current = int(self.grid.get(x, y))

        for nx, ny in self.grid.nearby_cells(x, y, include_diagonals=False):
            target = self.grid.get(nx, ny)

            if int(target) == current + 1:
                new_path_so_far = (path_so_far, (nx, ny)) if path_so_far is not None else None

                if target == '9':
                    found.add((nx, ny))

                    if found_paths is not None:
                        found_paths.add(new_path_so_far)
                else:
                    self._walk(nx, ny, found, new_path_so_far, found_paths)

    def part_1(self):
        for x, y in self.grid.locate_all('0'):
            found = set()
            self._walk(x, y, found)
            self.add_result(len(found))

    def part_2(self):
        for x, y in self.grid.locate_all('0'):
            found_paths = set()
            self._walk(x, y, set(), tuple(), found_paths)
            self.add_result(len(found_paths))


Day10(__file__).solve()

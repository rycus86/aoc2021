import os
import time
from typing import List, Dict, Set, Tuple, Iterable, Optional, Any


def var_sum(*args: int) -> int:
    return sum(args)


def var_mul(*args: int) -> int:
    result = 1
    for arg in args:
        result *= arg
    return result


class Grid(object):
    _neighbors = tuple((dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if abs(dx) != abs(dy))
    _neighbors_with_diagonals = tuple((dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx != 0 or dy != 0)

    def __init__(self, rows: List[Any]):
        self.rows = rows
        self.width = len(rows[0])
        self.height = len(rows)

    def get(self, x: int, y: int):
        return self.rows[y][x]

    def set(self, x: int, y: int, value: Any):
        row = self.rows[y]
        if isinstance(row, str):
            changed = row[0:x] + value + row[x + 1:]
        else:
            changed = row[0:x] + [value] + row[x + 1:]
        self.rows[y] = changed

    def rotate_left(self):
        rotated_rows = list(reversed(
            [self.get_column(x) for x in range(self.width)]
        ))
        return Grid(rotated_rows)

    def flip_y(self):
        return Grid(list(reversed(self.rows)))

    def flip_x(self):
        return Grid([list(reversed(row)) for row in self.rows])

    def get_row(self, y: int) -> List[Any]:
        return list(self.rows[y])

    def get_column(self, x: int) -> List[Any]:
        return list(row[x] for row in self.rows)

    def nearby_cells(self, x: int, y: int, include_diagonals=False) -> Dict[Tuple[int, int], Any]:
        neighbors = dict()
        if include_diagonals:
            dx_dy = self._neighbors_with_diagonals
        else:
            dx_dy = self._neighbors

        for dx, dy in dx_dy:
            tx, ty = x + dx, y + dy

            if tx < 0 or tx >= self.width:
                continue
            if ty < 0 or ty >= self.height:
                continue

            neighbors[(tx, ty)] = self.get(tx, ty)

        return neighbors

    def count(self, item):
        return sum(row.count(item) for row in self.rows)

    def locate(self, item):
        for row, items in enumerate(self.rows):
            if item in items:
                return items.index(item), row

    def locate_all(self, item):
        for row, items in enumerate(self.rows):
            if item in items:
                yield items.index(item), row

    def fill(self, item):
        for idx in range(len(self.rows)):
            self.rows[idx] = [item] * self.width
        return self

    def clone(self):
        return Grid(list(list(row) for row in self.rows))

    def to_string(self):
        return '\n'.join(''.join(map(str, row)) for row in self.rows)

    def print(self):
        for row in self.rows:
            print(''.join(map(str, row)))

    @classmethod
    def parse(cls, rows: List[Any]):
        return Grid(rows)

    @classmethod
    def empty(cls, width, height):
        return Grid([[0] * width] * height)


class Cube(object):
    _neighbors = tuple((dx, dy, dz)
                       for dx in (-1, 0, 1)
                       for dy in (-1, 0, 1)
                       for dz in (-1, 0, 1)
                       if dx != 0 or dy != 0 or dz != 0)

    _points: Dict[Tuple[int, int, int], Any]
    min_x: Optional[int]
    max_x: Optional[int]
    min_y: Optional[int]
    max_y: Optional[int]
    min_z: Optional[int]
    max_z: Optional[int]

    def __init__(self):
        self._points = dict()
        self.min_x = self.max_x = None
        self.min_y = self.max_y = None
        self.min_z = self.max_z = None

    def iter_items(self) -> Iterable[Tuple[Tuple[int, int, int], Any]]:
        for (x, y, z), item in self._points.items():
            yield (x, y, z), item

    def get(self, x: int, y: int, z: int, default=None):
        return self._points.get((x, y, z), default)

    def set(self, x: int, y: int, z: int, value: Any):
        self._points[(x, y, z)] = value

        if self.min_x is None:
            self.min_x = self.max_x = x
            self.min_y = self.max_y = y
            self.min_z = self.max_z = z
        else:
            self.min_x, self.max_x = min(x, self.min_x), max(x, self.max_x)
            self.min_y, self.max_y = min(y, self.min_y), max(y, self.max_y)
            self.min_z, self.max_z = min(z, self.min_z), max(z, self.max_z)

    def nearby_cells(self, x: int, y: int, z: int) -> Dict[Tuple[int, int, int], Any]:
        neighbors = dict()

        for dx, dy, dz in self._neighbors:
            tx, ty, tz = x + dx, y + dy, z + dz
            neighbors[(tx, ty, tz)] = self._points.get((tx, ty, tz))

        return neighbors


class CubeN(object):
    _points: Dict[Tuple, Any]
    _neighbors: List[List[int]]

    dimensions: int
    minimums: Dict[int, int]
    maximums: Dict[int, int]

    def __init__(self, dimensions=3):
        self.dimensions = dimensions
        self._points = dict()

        self.minimums = {i: None for i in range(dimensions)}
        self.maximums = {i: None for i in range(dimensions)}

        self._neighbors = list()

        for nb in range(3 ** dimensions):
            item = list()
            for d in range(dimensions):
                item.append(nb % 3 - 1)
                nb //= 3

            if item.count(0) != dimensions:
                self._neighbors.append(item)

    def iter_items(self) -> Iterable[Tuple[Tuple, Any]]:
        for position, item in self._points.items():
            yield position, item

    def get(self, *coordinates: int, default=None):
        return self._points.get(coordinates, default)

    def set(self, *coordinates: int, value: Any):
        self._points[coordinates] = value

        if self.minimums[0] is None:
            for idx, value in enumerate(coordinates):
                self.minimums[idx] = value
                self.maximums[idx] = value
        else:
            for idx, value in enumerate(coordinates):
                self.minimums[idx] = min(value, self.minimums[idx])
                self.maximums[idx] = max(value, self.maximums[idx])

    def nearby_cells(self, *coordinates: int) -> Dict[Tuple, Any]:
        neighbors = dict()

        for dc in self._neighbors:
            target = tuple(coordinates[idx] + dc[idx] for idx in range(self.dimensions))
            neighbors[target] = self._points.get(target)

        return neighbors

    def min(self, dimension_index):
        return self.minimums[dimension_index]

    def max(self, dimension_index):
        return self.maximums[dimension_index]


class Solution(object):
    input: str
    _counted_results: Optional[int]

    def __init__(self, solution_file=__file__, input_filename='input.txt'):
        self.input = self.read_input(solution_file, input_filename)
        self._counted_results = None

    def setup(self):
        pass

    def reset(self):
        self._counted_results = None

    def add_result(self, count=1):
        if self._counted_results is None:
            self._counted_results = count
        else:
            self._counted_results += count

    def max_result(self, value):
        if self._counted_results is None:
            self._counted_results = value
        else:
            self._counted_results = max(self._counted_results, value)

    def min_result(self, value):
        if self._counted_results is None:
            self._counted_results = value
        else:
            self._counted_results = min(self._counted_results, value)

    def part_1(self):
        print('<no part1 yet>')

    def part_2(self):
        print('<no part2 yet>')

    def solve(self):
        t0 = time.time()
        self.setup()
        setup_time = time.time() - t0
        if setup_time >= 1:
            print(f'Setup time: {setup_time:.2f} seconds')

        t1 = time.time()
        part_1 = self.part_1()
        if part_1 is not None:
            print(f'Part 1 result: {part_1}')
            print(f'  time: {time.time() - t1 + setup_time:.2f} seconds')
        elif self._counted_results is not None:
            print(f'Part 1 result: {self._counted_results}')
            print(f'  time: {time.time() - t1 + setup_time:.2f} seconds')

        self.reset()

        t0 = time.time()
        self.setup()
        setup_time = time.time() - t0
        if setup_time >= 1:
            print(f'Setup time: {setup_time:.2f} seconds')

        t2 = time.time()
        part_2 = self.part_2()
        if part_2 is not None:
            print(f'Part 2 result: {part_2}')
            print(f'  time: {time.time() - t2 + setup_time:.2f} seconds')
        elif self._counted_results is not None:
            print(f'Part 2 result: {self._counted_results}')
            print(f'  time: {time.time() - t2 + setup_time:.2f} seconds')

    def input_lines(self) -> List[str]:
        return self.input.splitlines(keepends=False)

    def input_grid(self) -> Grid:
        return Grid(self.input_lines())

    @staticmethod
    def read_input(solution_file, input_filename='input.txt') -> str:
        target_path = os.path.join(os.path.dirname(solution_file), input_filename)
        if os.path.exists(target_path):
            with open(target_path, 'r') as input_file:
                return input_file.read()

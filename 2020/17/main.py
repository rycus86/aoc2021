from shared.utils import *


class Day17(Solution):
    cube: CubeN

    def part_1(self):
        self.cube = self.read_cube(3)

        for _ in range(6):
            to_change = dict()

            for z in range(self.cube.min(2) - 1, self.cube.max(2) + 2):
                for y in range(self.cube.min(1) - 1, self.cube.max(1) + 2):
                    for x in range(self.cube.min(0) - 1, self.cube.max(0) + 2):
                        self.collect_changes(to_change, x, y, z)

            self.apply_changes(to_change)

        self.count_results()

    def part_2(self):
        self.cube = self.read_cube(4)

        for _ in range(6):
            to_change = dict()

            for w in range(self.cube.min(3) - 1, self.cube.max(3) + 2):
                for z in range(self.cube.min(2) - 1, self.cube.max(2) + 2):
                    for y in range(self.cube.min(1) - 1, self.cube.max(1) + 2):
                        for x in range(self.cube.min(0) - 1, self.cube.max(0) + 2):
                            self.collect_changes(to_change, x, y, z, w)

            self.apply_changes(to_change)

        self.count_results()

    def read_cube(self, dimensions):
        cube = CubeN(dimensions)

        for y, row in enumerate(self.input_lines()):
            for x, cell in enumerate(row):
                key = (x, y) + (0,) * (dimensions - 2)
                cube.set(*key, value=cell)

        return cube

    def collect_changes(self, changes: Dict[Tuple, Any], *coordinates: int):
        state = self.cube.get(*coordinates, default='.')
        neighbors = self.cube.nearby_cells(*coordinates)
        active_neighbors = list(neighbors.values()).count('#')

        if state == '#':
            if active_neighbors < 2 or active_neighbors > 3:
                changes[coordinates] = '.'
        else:  # state == '.'
            if active_neighbors == 3:
                changes[coordinates] = '#'

    def apply_changes(self, changes: Dict[Tuple, Any]):
        for coordinates, state in changes.items():
            self.cube.set(*coordinates, value=state)

    def count_results(self):
        for _, value in self.cube.iter_items():
            if value == '#':
                self.add_result()


Day17(__file__).solve()

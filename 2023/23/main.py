import sys

from shared.utils import *


class HikeGrid(Grid):
    _neighbors = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def nearby_cells(self, x: int, y: int, **kwargs) -> Dict[Tuple[int, int], Any]:
        nearby = dict()

        current = self.get(x, y)
        if current == '.':
            for (x, y), value in super().nearby_cells(x, y).items():
                if value != '#':
                    nearby[(x, y)] = value
        elif current == '>':
            nearby[(x + 1, y)] = self.get(x + 1, y)
        elif current == '<':
            nearby[(x - 1, y)] = self.get(x - 1, y)
        elif current == 'v':
            nearby[(x, y + 1)] = self.get(x, y + 1)
        elif current == '^':
            nearby[(x, y - 1)] = self.get(x, y - 1)

        return nearby


class Day23(Solution):
    grid: Grid
    target: Tuple[int, int]

    def setup(self):
        self.grid = HikeGrid(self.input_grid().rows)
        self.target = (self.grid.width - 2, self.grid.height - 1)

    def part_1(self):
        distances = self.walk_path(1, 0, {self.target})
        return distances[self.target]

    def part_2(self):
        # use the input grid here without the custom neighbour logic for wall counting
        ig = self.input_grid()

        junctions = {(1, 0), self.target}

        for x in range(ig.width):
            for y in range(ig.height):
                if ig.get(x, y) != '#':
                    # reset slopes to regular paths
                    self.grid.set(x, y, '.')
                    # collect junctions with 0 or 1 walls next to them
                    if tuple(ig.nearby_cells(x, y).values()).count('#') < 2:
                        junctions.add((x, y))

        # collect pairwise distances between junctions
        jj_distances = defaultdict(dict)
        for x, y in junctions:
            for j2, distance in self.walk_path(x, y, junctions).items():
                j1 = x, y
                jj_distances[j1][j2] = distance
                jj_distances[j2][j1] = distance

        # remember longest paths for sets of junctions so far
        cache = dict()

        queue = [(0, 1, 0, set())]
        while queue:
            length, x, y, visited = queue.pop(0)

            key = tuple(sorted(visited))
            if cache.get(key, -1) > length:
                continue  # we already found a longer path here
            else:
                cache[key] = length

            for (nx, ny), distance in jj_distances[(x, y)].items():
                if (nx, ny) in visited:
                    continue

                if (nx, ny) == self.target:
                    self.max_result(length + distance)
                    continue

                queue.insert(0, (length + distance, nx, ny, visited.union({(x, y)})))

    def walk_path(self, x, y, targets: Set[Tuple[int, int]]):
        queue = [(0, x, y)]

        visited = {(x, y)}
        distances = dict()

        while queue:
            length, x, y = queue.pop(0)

            for nx, ny in self.grid.nearby_cells(x, y):
                if (nx, ny) in visited:
                    continue
                else:
                    visited.add((nx, ny))

                if (nx, ny) in targets:
                    distances[(nx, ny)] = length + 1
                    continue

                queue.insert(0, (length + 1, nx, ny))

        return distances


Day23(__file__).solve()

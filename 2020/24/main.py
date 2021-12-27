from shared.utils import *


class Day24(Solution):
    black_tiles: Set[Tuple[int, int]]
    neighbors = (
        # sw, se, nw, ne
        (-1, -1), (-1, 1), (1, -1), (1, 1),
        # e, w
        (2, 0), (-2, 0)
    )

    def part_1(self):
        flipped = set()

        for line in self.input_lines():
            coordinates = self.apply_instructions(line)
            if coordinates in flipped:
                self.add_result(-1)
                flipped.remove(coordinates)
            else:
                self.add_result()
                flipped.add(coordinates)

        self.black_tiles = flipped

    def apply_instructions(self, directions: str) -> Tuple[int, int]:
        x, y = 0, 0

        while directions:
            if directions[0] == 'e':
                x += 2
                directions = directions[1:]
            elif directions[0] == 'w':
                x -= 2
                directions = directions[1:]
            elif directions[0] == 'n':
                y += 1
                if directions[1] == 'e':
                    x += 1
                else:
                    x -= 1
                directions = directions[2:]
            elif directions[0] == 's':
                y -= 1
                if directions[1] == 'e':
                    x += 1
                else:
                    x -= 1
                directions = directions[2:]

        return x, y

    def part_2(self):
        for day in range(100):
            self.daily_flips()

        return len(self.black_tiles)

    def daily_flips(self):
        to_white, to_black = set(), set()
        white_tiles_to_check = set()

        for x, y in self.black_tiles:
            black_neighbors = set()

            for dx, dy in self.neighbors:
                target = (x + dx, y + dy)
                if target in self.black_tiles:
                    black_neighbors.add(target)
                else:
                    white_tiles_to_check.add(target)

            if len(black_neighbors) == 0 or len(black_neighbors) > 2:
                to_white.add((x, y))

        for x, y in white_tiles_to_check:
            black_neighbors = set()

            for dx, dy in self.neighbors:
                target = (x + dx, y + dy)
                if target in self.black_tiles:
                    black_neighbors.add(target)

            if len(black_neighbors) == 2:
                to_black.add((x, y))

        self.black_tiles.difference_update(to_white)
        self.black_tiles.update(to_black)


Day24(__file__).solve()

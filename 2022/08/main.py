from shared.utils import *


class Day08(Solution):
    grid: Grid
    visible: Grid

    def setup(self):
        self.grid = Grid.parse(list(list(map(int, line)) for line in self.input_lines()))
        self.visible = Grid.empty(self.grid.width, self.grid.height)

        for y in range(self.grid.height):
            row = self.grid.get_row(y)

            current = -1
            for x, tree in enumerate(row):  # left to right
                if tree > current:
                    self.visible.set(x, y, 1)
                    current = tree

            current = -1
            for x, tree in reversed(list(enumerate(row))):  # right to left
                if tree > current:
                    self.visible.set(x, y, 1)
                    current = tree

        for x in range(self.grid.width):
            column = self.grid.get_column(x)

            current = -1
            for y, tree in enumerate(column):  # top to bottom
                if tree > current:
                    self.visible.set(x, y, 1)
                    current = tree

            current = -1
            for y, tree in reversed(list(enumerate(column))):  # bottom to top
                if tree > current:
                    self.visible.set(x, y, 1)
                    current = tree

    def part_1(self):
        return self.visible.count(1)

    def part_2(self):
        for x in range(1, self.grid.width - 1):
            for y in range(1, self.grid.height - 1):
                if not self.visible.get(x, y):
                    continue

                self.max_result(self.compute_scenic_score(x, y))

    def compute_scenic_score(self, current_x, current_y):
        current = self.grid.get(current_x, current_y)

        x, score_left = current_x, 0
        while x > 0:  # go left
            x -= 1

            target = self.grid.get(x, current_y)
            if target <= current or x == 0:
                score_left += 1

            if target >= current:
                break

        x, score_right = current_x, 0
        while x < self.grid.width - 1:  # go right
            x += 1

            target = self.grid.get(x, current_y)
            if target <= current or x == self.grid.width - 1:
                score_right += 1

            if target >= current:
                break

        y, score_up = current_y, 0
        while y > 0:  # go up
            y -= 1

            target = self.grid.get(current_x, y)
            if target <= current or y == 0:
                score_up += 1

            if target >= current:
                break

        y, score_down = current_y, 0
        while y < self.grid.height - 1:  # go down
            y += 1

            target = self.grid.get(current_x, y)
            if target <= current or y == self.grid.height - 1:
                score_down += 1

            if target >= current:
                break

        return score_left * score_right * score_up * score_down


Day08(__file__).solve()

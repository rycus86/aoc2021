from shared.utils import *


class Day12(Solution):
    grid: Grid
    steps: Grid
    prev: Grid

    def setup(self):
        self.grid = Grid.parse(self.input_lines())
        self.steps = self.grid.clone().fill(-1)

    def part_1(self):
        start_x, start_y = self.grid.locate('S')
        self.walk(start_x, start_y, 0)

        end_x, end_y = self.grid.locate('E')
        return self.steps.get(end_x, end_y)

    def part_2(self):
        best = 10**10

        start_x, start_y = self.grid.locate('S')
        self.walk(start_x, start_y, 0)

        end_x, end_y = self.grid.locate('E')
        best = self.steps.get(end_x, end_y)

        for x, y in self.grid.locate_all('a'):
            self.steps.fill(-1)
            self.walk(x, y, 0)
            best = min(best, self.steps.get(end_x, end_y))

        return best

    def walk(self, start_x, start_y, start_steps):
        to_visit = [(start_x, start_y, start_steps)]

        while to_visit:
            x, y, steps = to_visit.pop(0)

            if self.steps.get(x, y) >= steps:
                continue
            else:
                self.steps.set(x, y, steps)

            height, nb_heights = self.grid.get(x, y), self.grid.nearby_cells(x, y)
            nb_steps = self.steps.nearby_cells(x, y)

            if height == 'E':
                height = 'z'
            elif height == 'S':
                height = 'a'

            for (nb_x, nb_y), nb_h in nb_heights.items():
                if nb_h == 'E':
                    nb_h = 'z'
                elif nb_h == 'S':
                    nb_h = 'a'

                if ord(height) >= ord(nb_h) or ord(height) == ord(nb_h) - 1:
                    nb_s = nb_steps[(nb_x, nb_y)]
                    if 0 <= nb_s <= steps + 1:
                        pass
                    else:
                        to_visit.append((nb_x, nb_y, steps + 1))


Day12(__file__).solve()

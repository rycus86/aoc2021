import functools

from shared.utils import *


class Day21(Solution):
    grid: Grid
    start_x: int
    start_y: int

    def setup(self):
        self.grid = self.input_grid()
        self.start_x, self.start_y = self.grid.locate('S')

    def part_1(self):
        queue = {(self.start_x, self.start_y)}
        for _ in range(64):
            steps, queue = list(queue), set()
            while steps:
                cx, cy = steps.pop(0)
                for x, y in self.grid.nearby_cells(cx, cy):
                    if self.grid.get(x, y) != '#':
                        queue.add((x, y))

        return len(queue)

    def part_2(self):
        @functools.cache
        def next_steps(cx, cy):
            steps = set()
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                x, y = cx + dx, cy + dy
                if self.grid.get(x % self.grid.width, y % self.grid.height) != '#':
                    steps.add((x, y))
            return steps

        target_steps = 26501365

        prev_reached_per_grid = dict()
        reached_per_grid = dict()
        base_steps = 0

        ii, queue = 0, {(self.start_x, self.start_y)}

        while True:
            steps, queue = set(queue), set()
            for cx, cy in steps:
                queue.update(next_steps(cx, cy))

            ii += 1

            if ii % self.grid.width == target_steps % self.grid.width:
                pass
            else:
                continue  # avoid the rest of the computation

            # additional grid coordinates to generate
            grid_offset = tuple(range(-4, 5))
            # how many reached per grid
            reached_per_grid = defaultdict(int)
            for dx in grid_offset:
                for dy in grid_offset:
                    x1, y1 = dx * self.grid.width, dy * self.grid.height
                    x2, y2 = x1 + self.grid.width, y1 + self.grid.height
                    sum_reached = sum(1 for x, y in queue if x1 <= x < x2 and y1 <= y < y2)
                    if sum_reached:
                        reached_per_grid[sum_reached] += 1

            if len(prev_reached_per_grid) == len(reached_per_grid):
                base_steps = ii // self.grid.width
                # we have enough information now
                break
            else:
                prev_reached_per_grid = reached_per_grid

        # assemble the formula
        step_increment = (target_steps + 1) // self.grid.width
        result = 0

        # this is how many targets we reached in a single grid, with how many grids we saw that number in
        #   note: this worked for my input but not for the example, maybe this would need some further generalisation
        for num_reached, num_grids in reached_per_grid.items():
            if num_grids == prev_reached_per_grid[num_reached]:
                # this is constant regardless of how many grids we had in total
                result += num_reached

            elif num_grids == 1 + prev_reached_per_grid[num_reached]:
                # this increases by one with a step count equal to the initial grid size
                #  - (base_steps - num_grids) adjusts it by one if this pattern only start later
                result += (step_increment - (base_steps - num_grids)) * num_reached

            elif num_grids == 2 + prev_reached_per_grid[num_reached]:
                # this increases by two with a step count equal to the initial grid size (double the above)
                result += (step_increment - (base_steps - num_grids // 2)) * 2 * num_reached

            elif num_grids in (base_steps**2, (base_steps-1)**2):
                # this increases quadratically with a step count equal to the initial grid size
                baseline = 0
                if num_grids == (base_steps - 1) ** 2:
                    baseline -= 1
                result += (step_increment + baseline) ** 2 * num_reached

        return result


Day21(__file__).solve()

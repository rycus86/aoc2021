import math
from collections import Counter, defaultdict

from shared.utils import *


class Day20(Solution):
    tiles: Dict[int, Grid]
    w: int
    h: int

    def setup(self):
        self.tiles = dict()

        for part in self.input.split('\n\n'):
            title, data = part.splitlines()[0], part.splitlines()[1:]
            title = int(title.replace(':', '').split(' ')[1])
            grid = Grid(data)

            self.tiles[title] = grid
            self.w = grid.width
            self.h = grid.height

    def part_1(self):
        id_to_grid = list(self.tiles.items())
        matches = Counter()

        for i, (ref_id, reference) in enumerate(id_to_grid):
            for j, (target_id, target) in enumerate(id_to_grid[i + 1:]):
                if self.have_matching_edge(ref_id, target_id):
                    matches[ref_id] += 1
                    matches[target_id] += 1

        result = 1
        for key, neighbors in matches.items():
            if neighbors == 2:
                result *= key

        return result

    def have_matching_edge(self, reference: int, target: int) -> bool:
        """
        Check if tiles with the given IDs have any matching edges at all.
        """

        r_edges = self.get_all_edges(self.tiles[reference])
        t_edges = self.get_all_edges(self.tiles[target])

        for r_edge in r_edges:
            for t_edge in t_edges:
                if r_edge == t_edge or r_edge == list(reversed(t_edge)):
                    return True

    def get_all_edges(self, grid, also_reverse=False):
        """
        Return all edges of the grid (and optionally their reverse too).
        """

        r_top, r_bottom = grid.get_row(0), grid.get_row(self.h - 1)
        r_left, r_right = grid.get_column(0), grid.get_column(self.w - 1)
        if also_reverse:
            return r_top, r_bottom, r_left, r_right, \
                   list(reversed(r_top)), list(reversed(r_bottom)), list(reversed(r_left)), list(reversed(r_right))
        else:
            return r_top, r_bottom, r_left, r_right

    def part_2(self):
        id_to_grid = list(self.tiles.items())
        matches = defaultdict(set)

        # calculate matching neighbors
        for i, (ref_id, reference) in enumerate(id_to_grid):
            for j, (target_id, target) in enumerate(id_to_grid[i + 1:]):
                if self.have_matching_edge(ref_id, target_id):
                    matches[ref_id].add(target_id)
                    matches[target_id].add(ref_id)

        ggwh = int(math.sqrt(len(self.tiles)))
        grid_ids = Grid([[None] * ggwh] * ggwh)
        grid_of_grids = Grid([[None] * ggwh] * ggwh)

        # pick a top left
        top_left = next(i for i, m in matches.items() if len(m) == 2)
        grid_ids.set(0, 0, top_left)
        grid_of_grids.set(0, 0, self.tiles[top_left])

        # rotate the top left to have its neighbors below and to the right
        self.rotate_top_left(grid_ids, grid_of_grids, matches)
        # sort out the top row, starting from the known top left
        self.fill_top_row(grid_ids, grid_of_grids, matches)
        # sort out each column, starting from the known top tile
        for column in range(grid_ids.width):
            self.fill_column(column, grid_ids, grid_of_grids, matches)
        # remove the borders from each of the tiles
        self.remove_borders(grid_of_grids)
        # merge all tiles into a single big tile
        merged = self.merge_grids(grid_of_grids)
        # rotate the tile and find sea monsters, then return the result
        return self.calculate_result(merged)

    def rotate_top_left(self, grid_ids: Grid, grid_of_grids: Grid, matches: Dict[int, Set[int]]):
        """
        Rotate the top left (at 0x0) until it has the matching sides with its neighbors to the right and bottom.
        """

        tl_id, top_left = grid_ids.get(0, 0), grid_of_grids.get(0, 0)

        id_a, id_b = matches[grid_ids.get(0, 0)]
        a, b = self.tiles[id_a], self.tiles[id_b]

        a_edges = self.get_all_edges(a, True)
        b_edges = self.get_all_edges(b, True)

        for _ in range(2):
            for _ in range(4):
                if top_left.get_column(self.w - 1) in a_edges and top_left.get_row(self.h - 1) in b_edges:
                    grid_ids.set(1, 0, id_a)
                    grid_ids.set(0, 1, id_b)
                    grid_of_grids.set(0, 0, top_left.clone())
                    return
                else:
                    top_left = top_left.rotate_left()

            top_left = top_left.flip_y()

        raise Exception('should have figured out how to rotate by now')

    def fill_top_row(self, grid_ids: Grid, grid_of_grids: Grid, matches: Dict[int, Set[int]]):
        """
        Find and rotate the tiles in the top row, starting from the left.
        """

        previous = grid_of_grids.get(0, 0)
        target_column = previous.get_column(self.w - 1)

        for idx in range(1, grid_ids.width):
            g_id = grid_ids.get(idx, 0)
            grid = self.tiles.get(g_id)

            for _ in range(2):
                for _ in range(4):
                    if grid.get_column(0) == target_column:
                        grid = grid.clone()
                        grid_of_grids.set(idx, 0, grid)

                        # find the next one to the right
                        if idx < grid_ids.width - 1:
                            previous = grid
                            target_column = previous.get_column(self.w - 1)

                            for next_id in matches[g_id]:
                                if target_column in self.get_all_edges(self.tiles[next_id], True):
                                    grid_ids.set(idx + 1, 0, next_id)
                                    break

                        break
                    else:
                        grid = grid.rotate_left()

                if grid_of_grids.get(idx, 0) is not None:
                    break

                grid = grid.flip_y()

            else:
                raise Exception('should have figured out how to rotate by now')

    def fill_column(self, column: int, grid_ids: Grid, grid_of_grids: Grid, matches: Dict[int, Set[int]]):
        """
        Find and rotate tiles in the given column, going down starting from the top tile.
        """

        prev_id, previous = grid_ids.get(column, 0), grid_of_grids.get(column, 0)
        target_row = previous.get_row(self.h - 1)

        for idx in range(1, grid_ids.height):
            for g_id in matches[prev_id]:
                if target_row in self.get_all_edges(self.tiles[g_id], True):
                    grid_ids.set(column, idx, g_id)
                    break

            g_id = grid_ids.get(column, idx)
            grid = self.tiles.get(g_id)

            for _ in range(2):
                for _ in range(4):
                    if grid.get_row(0) == target_row:
                        grid = grid.clone()
                        grid_of_grids.set(column, idx, grid)

                        prev_id, previous = g_id, grid
                        target_row = previous.get_row(self.h - 1)
                        break
                    else:
                        grid = grid.rotate_left()

                if grid_of_grids.get(column, idx) is not None:
                    break

                grid = grid.flip_y()

            else:
                raise Exception('should have figured out how to rotate by now')

    def remove_borders(self, grid_of_grids: Grid):
        """
        Remove one cell around the tile (its border) for each tiles.
        """

        for y in range(grid_of_grids.height):
            for x in range(grid_of_grids.width):
                grid = grid_of_grids.get(x, y)
                grid_of_grids.set(x, y, Grid([row[1:-1] for row in grid.rows[1:-1]]))

    def merge_grids(self, grid_of_grids: Grid) -> Grid:
        """
        Merge all tiles into a single big tile.
        """

        merged_rows = list()

        for gy in range(grid_of_grids.height):
            for y in range(grid_of_grids.get(0, gy).height):
                row = list()

                for gx in range(grid_of_grids.width):
                    grid = grid_of_grids.get(gx, gy)
                    row.extend(grid.get_row(y))

                merged_rows.append(row)

        return Grid(merged_rows)

    def calculate_result(self, grid):
        """
        Find sea monsters in the single big tile, rotating and flipping it as needed,
        then return the number of # characters as requested.
        """

        sea_monster = '''
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
        '''
        mask = set()
        for line_no, line in enumerate(sea_monster.splitlines()[1:-1]):
            for idx, item in enumerate(line):
                if item == '#':
                    mask.add((idx, line_no))

        # sea monster dimensions
        sw, sh = 20, 3

        max_sea_monsters, max_grid = 0, None

        for _ in range(2):
            for _ in range(4):
                num_sea_monsters = 0

                for y in range(grid.height - sh):
                    for x in range(grid.width - sw):
                        if all(grid.get(x + mx, y + my) == '#' for mx, my in mask):
                            num_sea_monsters += 1

                if num_sea_monsters:
                    if num_sea_monsters > max_sea_monsters:
                        max_sea_monsters, max_grid = num_sea_monsters, grid.clone()

                grid = grid.rotate_left()
            grid = grid.flip_y()

        assert max_sea_monsters > 0

        grid = max_grid

        for y in range(grid.height - sh):
            for x in range(grid.width - sw):
                if all(grid.get(x + mx, y + my) == '#' for mx, my in mask):
                    for mx, my in mask:
                        grid.set(x + mx, y + my, 'O')

        return grid.count('#')


Day20(__file__).solve()

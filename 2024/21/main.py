from shared.utils import *
from itertools import permutations
from functools import cache


class Day21(Solution):
    numpad = (
        '789',
        '456',
        '123',
        '_0A'
    )
    dirpad = (
        '_^A',
        '<v>'
    )
    codes: list

    def setup(self):
        self.codes = list(self.input_lines())

    def move_numpad(self, instruction, result='', sx=2, sy=3):
        if instruction == '':
            yield result
            return

        item, instruction = instruction[0], instruction[1:]
        ty = next(idx for idx, buttons in enumerate(self.numpad) if item in buttons)
        tx = self.numpad[ty].index(item)

        dx, dy = abs(sx - tx), abs(sy - ty)
        ni = dx * ('<' if tx < sx else '>') + dy * ('^' if ty < sy else 'v')

        for moves in set(permutations(ni, dx + dy)):

            is_illegal_move = False
            px, py = sx, sy
            for c in moves:
                if c == '<':
                    px -= 1
                elif c == '>':
                    px += 1
                elif c == '^':
                    py -= 1
                elif c == 'v':
                    py += 1
                if (px, py) == (0, 3):
                    is_illegal_move = True
                    break

            if is_illegal_move:
                continue

            yield from self.move_numpad(instruction, result + ''.join(moves) + 'A', tx, ty)

    @cache
    def find_numpad(self, key):
        y = next(idx for idx, buttons in enumerate(self.dirpad) if key in buttons)
        return self.dirpad[y].index(key), y

    @cache
    def find_dirpad(self, key):
        y = next(idx for idx, buttons in enumerate(self.dirpad) if key in buttons)
        return self.dirpad[y].index(key), y

    @cache
    def shortest(self, from_key, to_key, robot=1, num_robots=25):
        sx, sy = self.find_dirpad(from_key)
        tx, ty = self.find_dirpad(to_key)

        dx, dy = abs(sx - tx), abs(sy - ty)
        if robot >= num_robots:
            return dx + dy + 1

        ni = dx * ('<' if tx < sx else '>') + dy * ('^' if ty < sy else 'v')

        min_moves = math.inf
        for moves in set(permutations(ni, dx + dy)):

            is_illegal_move = False
            px, py = sx, sy
            for c in moves:
                if c == '<':
                    px -= 1
                elif c == '>':
                    px += 1
                elif c == '^':
                    py -= 1
                elif c == 'v':
                    py += 1
                if (px, py) == (0, 0):
                    is_illegal_move = True
                    break

            if is_illegal_move:
                continue

            skey = 'A'
            subtotal = 0
            for m in moves:
                subtotal += self.shortest(skey, m, robot=robot+1, num_robots=num_robots)
                skey = m
            subtotal += self.shortest(skey, 'A', robot=robot+1, num_robots=num_robots)

            if subtotal < min_moves:
                min_moves = subtotal

        return min_moves

    def calculate(self, num_robots):
        for code in self.codes:
            min_length = math.inf
            for item in self.move_numpad(code):
                start = 'A'
                total = 0
                for digit in item:
                    total += self.shortest(start, digit, num_robots=num_robots)
                    start = digit
                min_length = min(min_length, total)
            # print(f'{code}: {min_length}')
            self.add_result(min_length * int(code[:-1]))

    def part_1(self):
        self.calculate(num_robots=2)
        assert self._counted_results == 162740, f'it was {self._counted_results}'

    def part_2(self):
        self.calculate(num_robots=25)
        assert self._counted_results == 203640915832208, f'it was {self._counted_results}'


Day21(__file__).solve()

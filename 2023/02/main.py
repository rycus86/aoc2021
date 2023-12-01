from shared.utils import *


class Game:
    def __init__(self, line: str):
        main_parts = line.split(':')
        self.num = int(main_parts[0].replace('Game ', ''))
        self.rgb_max = {c: 0 for c in ('red', 'green', 'blue')}
        for draw in main_parts[1].split(';'):
            for part in draw.split(','):
                cnum, color = part.strip().split(' ')
                self.rgb_max[color] = max(int(cnum), self.rgb_max[color])


class Day02(Solution):
    games: List[Game]

    def setup(self):
        self.games = list(Game(line) for line in self.input_lines())

    def part_1(self):
        for game in self.games:
            if game.rgb_max.get('red', 0) > 12:
                continue
            elif game.rgb_max.get('green', 0) > 13:
                continue
            elif game.rgb_max.get('blue', 0) > 14:
                continue

            self.add_result(game.num)

    def part_2(self):
        for game in self.games:
            self.add_result(var_mul(*game.rgb_max.values()))


Day02(__file__).solve()

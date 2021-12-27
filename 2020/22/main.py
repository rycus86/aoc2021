from shared.utils import *


class InstantWin(BaseException):
    pass


class RecursiveCombat(object):
    player1: List[int]
    player2: List[int]
    _played_before: List[Tuple[List[int], List[int]]]

    def __init__(self, player1: List[int], player2: List[int]):
        self.player1 = player1[:]
        self.player2 = player2[:]
        self._played_before = list()

    def play(self):
        while self.player1 and self.player2:
            # check infinite recursion
            combined = (self.player1[:], self.player2[:])
            if combined in self._played_before:
                # raise InstantWin()
                self.player1.extend(self.player2)
                self.player2.clear()
                break
            else:
                self._played_before.append(combined)

            # draw new cards
            a, b = self.player1.pop(0), self.player2.pop(0)

            if len(self.player1) >= a and len(self.player2) >= b:
                # play a new sub-game
                sub_game = RecursiveCombat(self.player1[0:a], self.player2[0:b])

                try:
                    sub_game.play()
                    player1_won = sub_game.has_player1_won()
                except InstantWin:
                    player1_won = True

                if player1_won:
                    self.player1.extend([a, b])
                else:
                    self.player2.extend([b, a])

            else:
                # the winner is the higher-value card
                if a > b:
                    self.player1.extend([a, b])
                else:
                    self.player2.extend([b, a])

    def score(self) -> int:
        result = 0
        for idx, value in enumerate(reversed(self.player1 or self.player2)):
            result += value * (idx + 1)
        return result

    def has_player1_won(self):
        assert not self.player1 or not self.player2, f'the game has not finished yet: {self}'
        return self.player1 and not self.player2

    def __repr__(self):
        return f'P1{self.player1} P2{self.player2}'


class Day22(Solution):
    player1: List[int]
    player2: List[int]

    def setup(self):
        parts = self.input.split('\n\n')
        self.player1 = list(map(int, parts[0].splitlines()[1:]))
        self.player2 = list(map(int, parts[1].splitlines()[1:]))

    def part_1(self):
        while self.player1 and self.player2:
            a, b = self.player1.pop(0), self.player2.pop(0)
            if a > b:
                self.player1.extend([a, b])
            else:
                self.player2.extend([b, a])

        for idx, value in enumerate(reversed(self.player1 or self.player2)):
            self.add_result(value * (idx + 1))

    def part_2(self):
        game = RecursiveCombat(self.player1, self.player2)
        game.play()
        return game.score()


Day22(__file__).solve()

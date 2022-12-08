from shared.utils import *


class Position(object):
    x: int
    y: int

    def __init__(self, to_follow=None):
        self.x = 0
        self.y = 0
        self.to_follow = to_follow

    def move(self, direction):
        if direction == 'R':
            self.x += 1
        elif direction == 'L':
            self.x -= 1
        elif direction == 'D':
            self.y += 1
        elif direction == 'U':
            self.y -= 1

    def follow(self):
        head = self.to_follow

        if self.x < head.x - 1 and self.y < head.y - 1:
            self.x += 1
            self.y += 1
        elif self.x < head.x - 1 and self.y > head.y + 1:
            self.x += 1
            self.y -= 1
        elif self.x > head.x + 1 and self.y < head.y - 1:
            self.x -= 1
            self.y += 1
        elif self.x > head.x + 1 and self.y > head.y + 1:
            self.x -= 1
            self.y -= 1
        elif self.x < head.x - 1:
            self.x += 1
            self.y = head.y
        elif self.x > head.x + 1:
            self.x -= 1
            self.y = head.y
        elif self.y < head.y - 1:
            self.y += 1
            self.x = head.x
        elif self.y > head.y + 1:
            self.y -= 1
            self.x = head.x

    def current_position(self):
        return self.x, self.y


class Day09(Solution):

    def part_1(self):
        head = Position()
        tail = Position(to_follow=head)

        visited = set()
        visited.add(tail.current_position())

        for actions in self.input_lines():
            direction, amount = actions.split()
            for _ in range(int(amount)):
                head.move(direction)
                tail.follow()
                visited.add(tail.current_position())

        return len(visited)

    def part_2(self):
        head = Position()
        tails = list()

        to_follow = head
        for _ in range(9):
            item = Position(to_follow)
            tails.append(item)
            to_follow = item

        visited = set()
        visited.add(tails[-1].current_position())

        for actions in self.input_lines():
            direction, amount = actions.split()
            for _ in range(int(amount)):
                head.move(direction)
                for item in tails:
                    item.follow()
                visited.add(tails[-1].current_position())

        return len(visited)


Day09(__file__).solve()

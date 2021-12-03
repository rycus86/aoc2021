def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


class Grid(list):
    def move(self):
        return self.move_east() + self.move_south()

    def move_east(self):
        total_moves = 0
        for row_index, row in enumerate(self):
            moves = list()
            for idx, item in enumerate(row):
                if item == '>':
                    if idx < len(row) - 1 and row[idx + 1] == '.':
                        moves.append((idx, idx + 1))
                    elif idx == len(row) - 1 and row[0] == '.':
                        moves.append((idx, 0))

            row = list(row)
            for move_from, move_to in moves:
                row[move_from], row[move_to] = '.', row[move_from]
                total_moves += 1
            self[row_index] = ''.join(row)

        return total_moves

    def move_south(self):
        moves = list()
        for row_index, row in enumerate(self):
            for idx, item in enumerate(row):
                if item == 'v':
                    if row_index < len(self) - 1 and self[row_index + 1][idx] == '.':
                        moves.append((row_index, row_index + 1, idx))
                    elif row_index == len(self) - 1 and self[0][idx] == '.':
                        moves.append((row_index, 0, idx))

        for row_from, row_to, index in moves:
            self[row_to] = self[row_to][:index] + 'v' + self[row_to][index+1:]
            self[row_from] = self[row_from][:index] + '.' + self[row_from][index+1:]

        return len(moves)

    def print(self):
        for row in self:
            print(row)
        print()


if __name__ == '__main__':
    grid = Grid()

    for line in read_input().splitlines():
        grid.append(line)

    # grid.print()
    for idx in range(1000):
        if grid.move() == 0:
            # grid.print()
            print('Found at step', idx + 1)
            break
        # else:
            # grid.print()

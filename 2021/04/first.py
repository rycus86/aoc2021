
def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


def is_bingo(_board, _numbers):
    for row in _board:
        if sum(1 if num in row else 0 for num in _numbers) == 5:
            return True

    for column in range(5):
        _col = [row[column] for row in _board]
        if sum(1 if num in _col else 0 for num in _numbers) == 5:
            return True

    return False


def get_result(_board, _numbers):
    unused = 0

    for row in _board:
        unused += sum(num if num not in _numbers else 0 for num in row)

    return _numbers[-1] * unused


if __name__ == '__main__':
    all_lines = read_input().splitlines()
    numbers = list(map(int, all_lines[0].split(',')))

    start_line = 2
    boards = []

    while start_line < len(all_lines):
        board = [list(map(int, line.strip().replace('  ', ' ').split(' ')))
                 for line in all_lines[start_line:start_line+5]]
        boards.append(board)
        start_line += 6

    for slice_len in range(5, len(numbers)):
        sliced = numbers[:slice_len]

        for board in boards:
            if is_bingo(board, sliced):
                # print('bingo', sliced, board)
                print('result:', get_result(board, sliced))
                exit(0)

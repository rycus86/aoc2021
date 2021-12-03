
def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


if __name__ == '__main__':
    x, y, aim = 0, 0, 0
    for line in read_input().splitlines():
        direction, value = line.split(' ')
        if direction == 'forward':
            x += int(value)
            y += aim * int(value)
        elif direction == 'down':
            aim += int(value)
        elif direction == 'up':
            aim -= int(value)

    print(f'x={x} y={y} -- answer: {x*y}')

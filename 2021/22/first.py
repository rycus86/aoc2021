def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


if __name__ == '__main__':
    switches = {
        (x, y, z): False
        for x in range(-50, 51)
        for y in range(-50, 51)
        for z in range(-50, 51)
    }

    for line in read_input().splitlines():
        # print('processing:', line)

        on_off, line = line.split(' ')
        x, y, z = line.split(',')
        x1, x2 = map(int, x[2:].split('..'))
        y1, y2 = map(int, y[2:].split('..'))
        z1, z2 = map(int, z[2:].split('..'))

        for xi in range(max(-50, x1), min(50, x2)+1):
            for yi in range(max(-50, y1), min(50, y2)+1):
                for zi in range(max(-50, z1), min(50, z2)+1):
                    turn_on = on_off == 'on'
                    switches[(xi, yi, zi)] = turn_on

    print('result:', sum(1 for sw in switches.values() if sw))

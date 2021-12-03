
def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


if __name__ == '__main__':
    p1, p2, p3 = None, None, None
    result = 0

    previous = None
    current = None

    for line in read_input().splitlines():
        p1, p2, p3 = p2, p3, int(line)

        if p1 is not None:
            current = p1+p2+p3
            if previous is not None and current > previous:
                result += 1

        previous = current

    print(result)

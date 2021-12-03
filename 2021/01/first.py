
def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


if __name__ == '__main__':
    previous = None
    result = 0

    for line in read_input().splitlines():
        current = int(line)
        if previous is not None and current > previous:
            result += 1
        previous = current

    print(result)

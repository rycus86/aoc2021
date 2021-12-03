
def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()
    

PAIRS = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<'
}

SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}


if __name__ == '__main__':
    score = 0

    for line in read_input().splitlines(keepends=False):
        stack = []

        for c in line:
            if c in PAIRS:
                if PAIRS[c] != stack.pop():
                    score += SCORES[c]
                    break
            else:
                stack.append(c)

    print('result:', score)

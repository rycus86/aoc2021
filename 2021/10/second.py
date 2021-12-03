
def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()
    

PAIRS = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<'
}

REVERSED = {
    v: k for k, v in PAIRS.items()
}

SCORES = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


if __name__ == '__main__':
    scores = []

    for line in read_input().splitlines(keepends=False):
        stack = []

        for c in line:
            if c in PAIRS:
                if PAIRS[c] != stack.pop():
                    break
            else:
                stack.append(c)

        else:
            if stack:
                extra = 0
                for r in reversed(stack):
                    extra *= 5
                    extra += SCORES[REVERSED[r]]

                scores.append(extra)

    middle = (len(scores)-1) / 2
    result = list(sorted(scores))[int(middle)]

    print('result:', result)

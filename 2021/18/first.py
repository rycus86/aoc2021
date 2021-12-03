from typing import List


def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


class Marker(object):
    def __init__(self, current, index, parent, parent_index, level):
        self.current: list = current
        self.index: int = index
        self.parent: list = parent
        self.parent_index: int = parent_index
        self.level: int = level

    @property
    def value(self):
        return self.current[self.index]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.parent[self.parent_index]}'


def explode(items: List[Marker]):
    for idx, item in enumerate(items):
        if item.level == 4:
            # print('lvl4:', item, item.parent, item.parent[1], item.current)

            if item.parent_index == 0:
                if idx > 0:
                    items[idx-1].current[items[idx-1].index] += item.current[0]
                if isinstance(item.parent[1], list):
                    item.parent[1][0] += item.current[1]
                else:
                    item.parent[1] += item.current[1]
            else:
                if idx < len(items) - 2:
                    items[idx+2].current[items[idx+2].index] += item.current[1]
                if isinstance(item.parent[0], list):
                    item.parent[0][1] += item.current[0]
                else:
                    item.parent[0] += item.current[0]

            item.parent[item.parent_index] = 0
            return True


def split(items: List[Marker]):
    for item in items:
        if item.value >= 10:
            left = right = item.value // 2
            if item.value % 2 == 1:
                right += 1

            item.current[item.index] = [left, right]
            return True


def flatten(items: list, parent_list: list = None, parent_index: int = 0, output: list = None, level: int = 0):
    if output is None:
        output = list()

    for idx, item in enumerate(items):
        if isinstance(item, list):
            flatten(item, items, idx, output, level + 1)
        else:
            output.append(Marker(items, idx, parent_list, parent_index, level))

    return output


def magnitude(items: list):
    left, right = items
    if isinstance(left, list):
        left = magnitude(left)
    if isinstance(right, list):
        right = magnitude(right)
    return 3*left + 2*right


if __name__ == '__main__':
    numbers = list()
    for line in read_input().splitlines():
        numbers.append(eval(line))

    result = numbers.pop(0)

    while numbers:
        current = numbers.pop(0)

        result = [result, current]
        flattened = flatten(result)
        print('appended:', result)

        stop = False
        while not stop:
            stop = True
            if explode(flattened):
                print('exploded:', result)
                flattened = flatten(result)
                stop = False
            elif split(flattened):
                print('split   :', result)
                flattened = flatten(result)
                stop = False

    print('magnitude:', magnitude(result))


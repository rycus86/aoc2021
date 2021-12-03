from collections import defaultdict


def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


def traverse(edges: dict, start: str, visited: set, path: list):
    result = 0

    for target in sorted(edges[start]):
        new_visited = set(visited)

        if target == 'end':
            # print('winner:', ''.join(path))
            result += 1
            continue
        elif target in visited:
            continue
        elif 'aa' <= target <= 'zz':
            new_visited.add(target)

        result += traverse(edges, target, new_visited, path + [target])

    return result


if __name__ == '__main__':
    edges = defaultdict(set)

    for line in read_input().splitlines(keepends=False):
        a, b = line.split('-')
        edges[a].add(b)
        edges[b].add(a)

    print('result:', traverse(edges, 'start', {'start'}, []))

from collections import defaultdict


def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


def traverse(edges: dict, start: str, visited: set, allow_twice: str, path: list):
    result = []

    for target in sorted(edges[start]):
        new_visited = set(visited)
        new_allowed = allow_twice

        if target == 'end':
            # print(f'winner:', ''.join(path))
            result.append(''.join(path))
            continue
        elif target in visited:
            continue
        elif 'aa' <= target <= 'zz':
            if target == allow_twice:
                new_allowed = ''
            else:
                new_visited.add(target)

        result.extend(traverse(edges, target, new_visited, new_allowed, path + [target]))

    return result


if __name__ == '__main__':
    edges = defaultdict(set)

    small_ones = set()

    for line in read_input().splitlines(keepends=False):
        a, b = line.split('-')
        edges[a].add(b)
        edges[b].add(a)

        if a not in ('start', 'end') and 'aa' <= a <= 'zz':
            small_ones.add(a)
        if b not in ('start', 'end') and 'aa' <= b <= 'zz':
            small_ones.add(b)

    all_results = set()
    for small in small_ones:
        all_results.update(traverse(edges, 'start', {'start'}, small, []))
    print('result:', len(all_results))

import math


def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


def distances(beacons):
    results = dict()
    for ia in range(len(beacons) - 1):
        for ib in range(ia + 1, len(beacons)):
            a, b = beacons[ia], beacons[ib]
            distance = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)
            results[(ia, ib)] = distance
    return results


def scanner_distances(sc1, sc2):
    rc2 = {y: x for x, y in sc2.items()}

    mapping = dict()

    for pos, dist in sc1.items():
        if dist in rc2:
            pa1, pa2 = pos
            pb1, pb2 = rc2[dist]

            if pa1 not in mapping:
                mapping[pa1] = {pb1, pb2}
            elif isinstance(mapping[pa1], set):
                if pb1 in mapping[pa1]:
                    mapping[pa1] = pb1
                else:
                    mapping[pa1] = pb2

            if pa2 not in mapping:
                mapping[pa2] = {pb1, pb2}
            elif isinstance(mapping[pa2], set):
                if pb1 in mapping[pa2]:
                    mapping[pa2] = pb1
                else:
                    mapping[pa2] = pb2

    # drop unresolved ones
    mapping = {x: y for x, y in mapping.items() if isinstance(y, int)}

    return mapping


if __name__ == '__main__':
    scanners = list()
    current = list()

    for line in read_input().splitlines():
        if line.startswith('--- scanner '):
            if current:
                scanners.append(current)
            current = list()
        elif line.strip():
            current.append(list(map(int, line.split(','))))
    else:
        if current:
            scanners.append(current)

    transformed = dict()

    for si, scanner in enumerate(scanners):
        transformed[si] = distances(scanner)

    unique = set()
    matched = set()

    for si1, scanner1 in enumerate(scanners):
        for si2, scanner2 in enumerate(scanners):
            if si2 == si1:
                continue

            scd = scanner_distances(transformed[si1], transformed[si2])

            for sp1, sp2 in scd.items():
                key_1 = '%03d_%03d' % (si1, sp1)
                key_2 = '%03d_%03d' % (si2, sp2)

                if key_1 not in matched:
                    unique.add(key_1)

                matched.add(key_1)
                matched.add(key_2)

        for sitem in range(len(scanner1)):
            key = '%03d_%03d' % (si1, sitem)
            if key not in matched:
                unique.add(key)
                matched.add(key)

    print('result:', len(unique))

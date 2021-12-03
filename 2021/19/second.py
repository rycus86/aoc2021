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
            # results[(ia, ib)] = results[(ib, ia)] = distance
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


def compute_scanner_position(relative, target, matched_distances):
    r0, t0 = None, None
    translated = dict()
    multiplier = dict()

    for ri, ti in matched_distances.items():
        if r0 is None:
            r0, t0 = relative[ri], target[ti]
            continue

        rd = list((r0[i] - relative[ri][i]) for i in range(3))
        td = list((t0[i] - target[ti][i]) for i in range(3))

        # make sure these are all unique
        if len(set(td)) < 3:
            r0, t0 = relative[ri], target[ti]
            continue

        try:
            for rri, rrx in enumerate(rd):
                mul = 1
                if rrx not in td:
                    mul = -1

                translated[rri] = td.index(mul * rrx)
                multiplier[rri] = mul
        except ValueError:
            continue  # not super sure what's going on here

        tt = [multiplier[i] * t0[translated[i]] for i in range(3)]
        transformed_coordinates = list()
        for titem in target:
            transformed_coordinates.append([multiplier[i] * titem[translated[i]] for i in range(3)])

        # distance from 'relative' scanner, transformed scanner position in 'relative' coordinates
        return [r0[i] - tt[i] for i in range(3)], transformed_coordinates

    return None, None  # can this even happen?


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

    abs_scanner_pos = {0: [0, 0, 0]}
    translated_scanner = {0: [0, 1, 2]}
    multiplier_scanner = {0: [1, 1, 1]}

    for si1, scanner1 in enumerate(scanners):
        for si2, scanner2 in enumerate(scanners):
            if si2 == si1:
                continue

            scd = scanner_distances(transformed[si1], transformed[si2])

            if len(scd) > 1:
                csp, transformed_scanner = compute_scanner_position(scanner1, scanner2, scd)
                if csp is None:
                    continue

                if si1 in abs_scanner_pos:
                    scanners[si2] = transformed_scanner
                else:
                    continue  # we can't use these coordinates here

                if si2 not in abs_scanner_pos:
                    if si1 in abs_scanner_pos:
                        shifted = abs_scanner_pos[si1][:]
                        for shi in range(3):
                            shifted[shi] += csp[shi]
                        abs_scanner_pos[si2] = shifted

    # print('absolute:', abs_scanner_pos)
    # for x in sorted(abs_scanner_pos):
    #     print(x, abs_scanner_pos[x])

    max_distance = 0
    for si1, scanner1 in abs_scanner_pos.items():
        for si2, scanner2 in abs_scanner_pos.items():
            manhattan = sum(abs(scanner1[i] - scanner2[i]) for i in range(3))
            max_distance = max(manhattan, max_distance)

    print('result:', max_distance)

from shared.utils import *


class Day05(Solution):
    seeds: List[int]
    types: Dict[str, str]
    maps: Dict[str, Dict[Tuple[int, int], int]]

    def setup(self):
        self.seeds = list()
        self.types = dict()
        self.maps = dict()

        current_type = None

        for line in self.input_lines():
            if not line.strip():
                continue

            if not self.seeds:
                self.seeds = list(map(int, line.strip().replace('seeds: ', '').split(' ')))
                continue

            if ' map:' in line:
                tfrom, tto = line.replace(' map:', '').strip().split('-to-')
                self.types[tfrom] = tto
                self.maps[tfrom] = dict()
                current_type = tfrom
                continue

            n_dest, n_source, n_range = map(int, line.split(' '))
            self.maps[current_type][(n_source, n_range)] = n_dest

    def part_1(self):
        min_loc = 10**10

        for seed in self.seeds:
            current_type = 'seed'
            target = seed

            while current_type != 'location':
                for (n_source, n_range), n_dest in self.maps[current_type].items():
                    if n_source <= target < n_source + n_range:
                        target += n_dest - n_source
                        break

                current_type = self.types[current_type]

            min_loc = min(min_loc, target)

        return min_loc

    def part_2(self):
        ranges = list()  # type: List[Interval]

        for idx in range(0, len(self.seeds) // 2 + 1, 2):
            s, r = self.seeds[idx], self.seeds[idx+1]
            ranges.append(Interval(s, s + r, 'seed'))

        ranges = list(sorted(ranges))

        current_type = 'seed'
        while current_type != 'location':
            target_type = self.types[current_type]

            for (n_source, n_range), n_dest in self.maps[current_type].items():
                ni = Interval(n_source, n_source + n_range, target_type)

                new_ranges = list()
                for r in ranges:

                    if r.data == current_type:  # only process intervals we have not split yet
                        to_add = list()
                        for s in r.split(ni):
                            to_add.append(s)

                            if s.data == target_type:
                                # if this split to the new type, adjust to the destination coordinates
                                s.start += n_dest - n_source
                                s.end += n_dest - n_source

                        new_ranges.extend(to_add)

                    elif r.data == target_type:  # if this was already the new type, just keep it
                        new_ranges.append(r)

                ranges = list(sorted(new_ranges))

            for r in ranges:
                # any items still on the old type should just carry over as the new type
                r.data = target_type

            current_type = target_type

        return ranges[0].start


Day05(__file__).solve()

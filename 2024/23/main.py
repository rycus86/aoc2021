from shared.utils import *


class Day23(Solution):
    connections: dict[str, set[str]]

    def setup(self):
        self.connections = defaultdict(set)

        for line in self.input_lines():
            a, b = line.split('-')
            self.connections[a].add(b)
            self.connections[b].add(a)

    def part_1(self):
        groups = set()

        for pc, links in self.connections.items():
            if pc[0] != 't':
                continue

            slinks = list(sorted(links))
            for idx, link1 in enumerate(slinks):
                for link2 in slinks[idx+1:]:
                    if link2 in self.connections[link1]:
                        groups.add(tuple(sorted((pc, link1, link2))))

        return len(groups)

    def part_2(self):
        groups = set(self.connections.keys())

        for pc in self.connections:
            for group in groups:
                if all(pc in self.connections[g] for g in group.split(',')):
                    groups.remove(group)
                    groups.add(group + ',' + pc)

        largest_group = max(groups, key=len)
        return ','.join(sorted(largest_group.split(',')))


Day23(__file__).solve()

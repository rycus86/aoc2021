from collections import defaultdict

from shared.utils import *


class Day06(Solution):
    orbiters: Dict[str, Set[str]]

    def setup(self):
        self.orbiters = defaultdict(set)

        for line in self.input_lines():
            center, orbits = line.split(')')
            self.orbiters[orbits].add(center)

    def part_1(self):
        for planet in self.orbiters:
            self.count_orbits(planet)

    def part_2(self):
        me, santa = self.orbiters['YOU'], self.orbiters['SAN']
        my_connections = dict()

        my_index = 0
        while me:
            next_level = set()
            for planet in me:
                my_connections[planet] = my_index
                next_level.update(self.orbiters[planet])
            me = next_level
            my_index += 1

        santa_index = 0
        while santa:
            next_level = set()
            for planet in santa:
                if planet in my_connections:
                    return my_connections[planet] + santa_index
                else:
                    next_level.update(self.orbiters[planet])
            santa = next_level
            santa_index += 1


    def count_orbits(self, planet):
        if planet not in self.orbiters:
            return

        self.add_result()

        for child in self.orbiters[planet]:
            self.count_orbits(child)


Day06(__file__).solve()

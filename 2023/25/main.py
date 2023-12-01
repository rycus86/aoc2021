import networkx as nx

from shared.utils import *


class Day25(Solution):
    graph: nx.Graph
    nodes: Set[str]

    def setup(self):
        self.graph = nx.Graph()
        self.nodes = set()

        for line in self.input_lines():
            key, targets = line.split(':')
            self.nodes.add(key)

            targets = targets.strip().split()
            for target in targets:
                self.graph.add_edge(key, target, capacity=1)
                self.nodes.add(target)

    def part_1(self):
        for a in self.nodes:
            for b in self.nodes:
                if a == b:
                    continue

                v, (s, t) = nx.minimum_cut(self.graph, a, b)
                if v == 3:
                    # when we cut edges totalling 3 capacity (e.g. 3 of 1 each) then we're good
                    return len(s) * len(t)

    def part_2(self):
        pass  # no part 2 here


Day25(__file__).solve()

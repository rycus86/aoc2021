from shared.utils import *


class Day20(Solution):
    modules: Dict[str, List[str]]
    flip_flops: Dict[str, int]
    conjunctions: Dict[str, Dict[str, int]]

    def setup(self):
        self.modules = dict()
        self.flip_flops = dict()
        self.conjunctions = dict()

        for line in self.input_lines():
            name, targets = line.split(' -> ')
            targets = list(map(str.strip, targets.split(',')))

            if name[0] == '%':
                name = name[1:]
                self.flip_flops[name] = 0
            elif name[0] == '&':
                name = name[1:]
                self.conjunctions[name] = dict()

            self.modules[name] = targets

        for source, targets in self.modules.items():
            for target in targets:
                if target in self.conjunctions:
                    self.conjunctions[target][source] = 0

    def part_1(self):
        low, high = 0, 0

        for _ in range(1000):

            queue = [('broadcaster', 0, None)]
            while queue:
                target, signal, source = queue.pop(0)

                if signal == 0:
                    low += 1
                else:
                    high += 1

                if target in self.flip_flops:
                    if signal == 1:
                        continue

                    self.flip_flops[target] = 1 - self.flip_flops[target]
                    signal = self.flip_flops[target]

                if target in self.conjunctions:
                    self.conjunctions[target][source] = signal

                    if all(1 == v for v in self.conjunctions[target].values()):
                        signal = 0
                    else:
                        signal = 1

                if target not in self.modules:
                    continue

                for m in self.modules[target]:
                    queue.append((m, signal, target))

        return low * high

    def part_2(self):
        """
         in my input, the final conjuction had 4 conjuctions as inputs, all 4 needed to send high
           to do so, each of them needed to receive low at the same time
           each of them had one conjuction as input, each need to receive high for all inputs to send low
           all of these conjuctions were connected to flip flops only, which all needed to send high at the same time
           so we keep track of the frequencies these flip flops send high, and find the lowest common index in them
        """

        # these need to receive high to send low
        final_conjunctions = [c for c in self.conjunctions if 'rx' in self.modules[c]]
        # these need to receive low to send high
        second_conjunctions = [c for c in self.conjunctions if any(fc in final_conjunctions for fc in self.modules[c])]
        # these all need to receive high at the same time to have all send low signals
        third_conjunctions = [c for c in self.conjunctions if any(sc in second_conjunctions for sc in self.modules[c])]
        # check we're done here
        fourth_conjunctions = [c for c in self.conjunctions if any(tc in third_conjunctions for tc in self.modules[c])]
        # ensure these all only depend on flip flops
        assert len(fourth_conjunctions) == 0
        # these are the flip flops we are interested in, which all need to send high at the same time
        target_flip_flops = set(ff for ff in self.flip_flops if any(tc in third_conjunctions for tc in self.modules[ff]))

        flip_flop_high_indexes = {ff: list() for ff in target_flip_flops}

        # checking frequencies up to 10000 is enough
        for idx in range(10000):
            queue = [('broadcaster', 0, None)]
            while queue:
                target, signal, source = queue.pop(0)

                if target in self.flip_flops:
                    if signal == 1:
                        continue

                    self.flip_flops[target] = 1 - self.flip_flops[target]
                    signal = self.flip_flops[target]

                    if signal == 1 and target in target_flip_flops:
                        flip_flop_high_indexes[target].append(idx)

                if target in self.conjunctions:
                    self.conjunctions[target][source] = signal

                    if all(1 == v for v in self.conjunctions[target].values()):
                        signal = 0
                    else:
                        signal = 1

                if target == 'rx':
                    continue

                for m in self.modules[target]:
                    queue.append((m, signal, target))

        signal_frequencies = set(map(self.calculate_frequency, flip_flop_high_indexes.values()))

        return math.lcm(*signal_frequencies)

    @staticmethod
    def calculate_frequency(indexes: List[int]):
        """
        the differences look like [X, X, X, Y, Z, X, X, X, Y, Z, ...]
          so the first distance repeats 1+ times, then one or more irregular distances, then it starts over
          the special case is where there are no irregular entries
        """

        differences = [value - indexes[idx] for idx, value in enumerate(indexes[1:])]

        # check if we only have one value for a regular frequency
        if len(set(differences)) == 1:
            return differences[0]

        # keep adding differences until we loop back to the starting difference
        start, result, initial_run = differences[0], 0, True
        for diff in differences:
            if diff != start:
                initial_run = False
            elif not initial_run:
                break

            result += diff

        return result


Day20(__file__).solve()

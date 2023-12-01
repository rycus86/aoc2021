from shared.utils import *


class Day15(Solution):
    steps: List[str]

    def setup(self):
        self.steps = self.input.strip().split(',')

    def part_1(self):
        for step in self.steps:
            self.add_result(self._hash(step))

    def part_2(self):
        hashmap = {idx: list() for idx in range(256)}  # type: Dict[int, List[Tuple[str, int]]]

        for step in self.steps:
            if '=' in step:
                label, flen = step.split('=')
                flen = int(flen)
            else:
                label, flen = step[:-1], -1

            box_idx = self._hash(label)
            values = hashmap[box_idx]

            if flen < 0:
                for idx, (el, _) in enumerate(list(values)):
                    if label == el:
                        del values[idx]
                        break

            else:
                for idx, (el, _) in enumerate(list(values)):
                    if label == el:
                        values[idx] = (label, flen)
                        break
                else:
                    values.append((label, flen))

        for box in range(256):
            for slot, (label, flen) in enumerate(hashmap[box]):
                self.add_result((box + 1) * (slot + 1) * flen)

    @staticmethod
    def _hash(s):
        value = 0
        for c in s:
            value = ((ord(c) + value) * 17) % 256
        return value


Day15(__file__).solve()

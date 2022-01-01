from typing import List


class IntCodeProgram(object):
    debug = False

    def __init__(self, program: List[int]):
        self.program = program[:]
        self.cursor = 0
        self._done = False

    def clone(self):
        return IntCodeProgram(self.program)

    def reset(self):
        self.cursor = 0

    def is_done(self):
        return self._done

    def run(self, given_inputs: List[int]):
        numbers = self.program

        while True:
            n = numbers[self.cursor]
            ia, ib = False, False

            if n > 99:
                ia = (n // 100) % 10 == 1
                ib = (n // 1000) % 10 == 1
                n = n % 10

            if n == 99:
                self._done = True
                return None

            if n == 1:
                a, b, c = numbers[self.cursor+1:self.cursor+4]
                va = a if ia else numbers[a]
                vb = b if ib else numbers[b]

                if self.debug:
                    print(f'{self.cursor:3d},{n}) n[{c:3d}] = {va} + {vb} = {va + vb}')

                numbers[c] = va + vb
                self.cursor += 4
            elif n == 2:
                a, b, c = numbers[self.cursor+1:self.cursor+4]
                va = a if ia else numbers[a]
                vb = b if ib else numbers[b]

                if self.debug:
                    print(f'{self.cursor:3d},{n}) n[{c:3d}] = {va} * {vb} = {va * vb}')

                numbers[c] = va * vb
                self.cursor += 4
            elif n == 3:
                a = numbers[self.cursor+1]
                assert 0 <= a < len(numbers), f'tried to read value into n[{a}]'
                numbers[a] = given_inputs.pop(0)

                if self.debug:
                    print(f'{self.cursor:3d},{n}) n[{a:3d}] = {numbers[a]} (read)')

                self.cursor += 2
            elif n == 4:
                a = numbers[self.cursor+1]
                # assert ia is False
                va = a if ia else numbers[a]

                if self.debug:
                    print(f'{self.cursor:3d},{n}) n[{a:3d}] = {va} (output)')

                self.cursor += 2
                return va
            elif n == 5:
                a, b = numbers[self.cursor+1:self.cursor+3]
                va = a if ia else numbers[a]
                vb = b if ib else numbers[b]

                if self.debug:
                    print(f'{self.cursor:3d},{n}) n[{a:3d}] = {va} != 0 : cursor[{self.cursor}] -> {vb if va != 0 else self.cursor + 3}')

                if va != 0:
                    self.cursor = vb
                else:
                    self.cursor += 3
            elif n == 6:
                a, b = numbers[self.cursor+1:self.cursor+3]
                va = a if ia else numbers[a]
                vb = b if ib else numbers[b]

                if self.debug:
                    print(f'{self.cursor:3d},{n}) n[{a:3d}] = {va} == 0 : cursor[{self.cursor}] -> {vb if va == 0 else self.cursor + 3}')

                if va == 0:
                    self.cursor = vb
                else:
                    self.cursor += 3
            elif n == 7:
                a, b, c = numbers[self.cursor+1:self.cursor+4]
                va = a if ia else numbers[a]
                vb = b if ib else numbers[b]

                numbers[c] = 1 if va < vb else 0
                if self.debug:
                    print(f'{self.cursor:3d},{n}) n[{c:3d}] = {va} < {vb} ? {numbers[c]}')

                self.cursor += 4
            elif n == 8:
                a, b, c = numbers[self.cursor+1:self.cursor+4]
                va = a if ia else numbers[a]
                vb = b if ib else numbers[b]

                numbers[c] = 1 if va == vb else 0
                if self.debug:
                    print(f'{self.cursor:3d},{n}) n[{c:3d}] = {va} == {vb} ? {numbers[c]}')

                self.cursor += 4

        return None

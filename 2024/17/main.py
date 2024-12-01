from shared.utils import *
from functools import cache
from dataclasses import dataclass


@dataclass
class Computer:
    pointer: int
    a: int
    b: int
    c: int

    def __hash__(self):
        return hash((self.pointer, self.a, self.b, self.c))

    def combo_value(self, op):
        if op == 4:
            return self.a
        elif op == 5:
            return self.b
        elif op == 6:
            return self.c
        else:
            return op

    def adv(self, op):
        self.a = self.a // (2 ** self.combo_value(op))

    def bxl(self, op):
        self.b = self.b ^ op

    def bst(self, op):
        self.b = self.combo_value(op) % 8

    def jnz(self, op):
        if self.a == 0:
            return
        else:
            self.pointer = op
            return 'jump', op

    def bxc(self, op):
        self.b = self.b ^ self.c

    def out(self, op):
        return 'print', self.combo_value(op) % 8

    def bdv(self, op):
        self.b = self.a // (2 ** self.combo_value(op))

    def cdv(self, op):
        self.c = self.a // (2 ** self.combo_value(op))

    def copy(self):
        return Computer(self.pointer, self.a, self.b, self.c)

class Day17(Solution):
    computer: Computer
    program: list[int]
    instructions: dict[int, any]

    def setup(self):
        self.instructions = {
            0: Computer.adv,
            1: Computer.bxl,
            2: Computer.bst,
            3: Computer.jnz,
            4: Computer.bxc,
            5: Computer.out,
            6: Computer.bdv,
            7: Computer.cdv
        }

        a, b, c = 0, 0, 0

        for line in self.input_lines():
            if line.startswith('Register A:'):
                a = int(line.split(':')[1].strip())
            elif line.startswith('Register B:'):
                b = int(line.split(':')[1].strip())
            elif line.startswith('Register C:'):
                c = int(line.split(':')[1].strip())
            elif line.startswith('Program:'):
                self.program = list(map(int, line.split(':')[1].strip().split(',')))

        self.computer = Computer(0, a, b, c)

    def part_1(self):
        values = list()
        while self.computer.pointer < len(self.program):
            instruction, operand = self.program[self.computer.pointer], self.program[self.computer.pointer + 1]
            self.computer.pointer += 2
            if (value := self.instructions[instruction](self.computer, operand)) is not None:
                code, result = value
                if code == 'print':
                    values.append(result)

        return ','.join(map(str, values))

    def part_2(self):
        def digit(a):
            b = a % 8
            b = b ^ self.program[3]
            c = a // 2**b
            # a = a // 2**3
            b = b ^ self.program[9]
            b = b ^ c
            return b % 8

        def check(ri, a):
            if digit(a) == self.program[-ri]:
                if ri == len(self.program):
                    yield a
                else:
                    for i in range(8):
                        yield from check(ri + 1, (a << 3) + i)

        return next(b for a in range(8) for b in check(1, a))

Day17(__file__).solve()

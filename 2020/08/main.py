from shared.utils import *


class Day08(Solution):
    instructions = List[Tuple[str, int]]
    jumps = List[int]

    def setup(self):
        self.instructions = list()
        self.jumps = list()

        for idx, line in enumerate(self.input_lines()):
            instruction, arg = line.split(' ')
            self.instructions.append((instruction, int(arg)))
            self.jumps.append(idx)

    def part_1(self):
        return self.play_program(self.instructions)

    def part_2(self):
        for idx in self.jumps:
            instructions = self.instructions[:]
            instructions[idx] = ('nop', 0)
            acc, finished = self.play_program(instructions, True)
            if finished:
                return acc

    def play_program(self, instructions, return_finished=False):
        idx, acc, executed = 0, 0, set()
        while idx < len(instructions) and idx not in executed:
            executed.add(idx)
            instruction, arg = instructions[idx]

            if instruction == 'nop':
                idx += 1
            elif instruction == 'acc':
                idx += 1
                acc += arg
            elif instruction == 'jmp':
                idx += arg
            else:
                raise Exception(f'unexpected instruction: {instruction}')

        if return_finished:
            return acc, idx not in executed
        else:
            return acc


Day08(__file__).solve()

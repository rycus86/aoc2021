from shared.utils import *


class Day10(Solution):
    instructions: List[Tuple[int, int]]  # add, steps

    def setup(self):
        self.instructions = list()

        for line in self.input_lines():
            if line.startswith('noop'):
                self.instructions.append((0, 1))
            elif line.startswith('addx '):
                value = int(line.split()[-1])
                self.instructions.append((value, 2))

    def part_1(self):
        current_value = 1
        current_step = 0

        for add, steps in self.instructions:
            current_step += steps

            eval_step = current_step
            if eval_step % 40 == 21 and steps == 2:
                eval_step -= 1

            if eval_step % 40 == 20:
                self.add_result(eval_step * current_value)

            current_value += add

    def part_2(self):
        current_value = 1
        currently_adding = 0
        steps_remaining = 0

        for step in range(240):
            if step % 40 == 0:
                print()

            if steps_remaining > 0:
                steps_remaining -= 1
            else:
                current_value += currently_adding
                add, steps = self.instructions.pop(0)
                currently_adding, steps_remaining = add, steps - 1

            if current_value - 1 <= step % 40 <= current_value + 1:
                print('#', end='')
            else:
                print(' ', end='')


Day10(__file__).solve()

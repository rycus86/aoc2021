from typing import Dict, List


def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


class Values(dict):
    def __hash__(self):
        return hash((self["w"], self["x"], self["y"], self["z"]))


class Instruction(object):
    def __init__(self, operator, var, *args):
        self.operator = operator
        self.var = var
        self.arg = args[0] if args else None
        self.invalid_configurations = set()

    def has_arg_number(self):
        return self.arg is not None and not ('w' <= self.arg <= 'z')

    def check_and_evaluate(self, values: Dict[str, int]):
        if values in self.invalid_configurations:
            return False
        else:
            self.invalid_configurations.add(values)

        self.evaluate(values)
        return True

    def evaluate(self, values: Dict[str, int]):
        raise Exception(f'unknown operator: {self.operator}')

    def debug(self, values):
        self.evaluate(values)
        return values[self.var]

    def __repr__(self):
        if self.arg is not None:
            return f'{self.__class__.__name__}({self.var} {self.arg})'
        else:
            return f'{self.__class__.__name__}({self.var})'

    @classmethod
    def parse(cls, *components):
        op = components[0]
        if op == 'inp':
            return Input(*components)
        elif op == 'add':
            return Add(*components)
        elif op == 'mul':
            return Multiply(*components)
        elif op == 'div':
            return Divide(*components)
        elif op == 'mod':
            return Modulo(*components)
        elif op == 'eql':
            return Equal(*components)


class Input(Instruction):
    start = 0
    seed = ''

    def evaluate(self, values: Dict[str, int]):
        if Input.seed:
            values[self.var], Input.seed = int(Input.seed[0]), Input.seed[1:]
        else:
            values[self.var] = Input.start


class Add(Instruction):
    def evaluate(self, values: Dict[str, int]):
        if self.has_arg_number():
            values[self.var] += int(self.arg)
        else:
            values[self.var] += values[self.arg]


class Multiply(Instruction):
    def evaluate(self, values: Dict[str, int]):
        if self.has_arg_number():
            values[self.var] *= int(self.arg)
        else:
            values[self.var] *= values[self.arg]


class Divide(Instruction):
    def evaluate(self, values: Dict[str, int]):
        if self.has_arg_number():
            values[self.var] //= int(self.arg)
        else:
            values[self.var] //= values[self.arg]


class Modulo(Instruction):
    def evaluate(self, values: Dict[str, int]):
        if self.has_arg_number():
            values[self.var] %= int(self.arg)
        else:
            values[self.var] %= values[self.arg]


class Equal(Instruction):
    def evaluate(self, values: Dict[str, int]):
        if self.has_arg_number():
            values[self.var] = 1 if values[self.var] == int(self.arg) else 0
        else:
            values[self.var] = 1 if values[self.var] == values[self.arg] else 0


def print_formula(instructions: List[Instruction], index):
    step_4_div_z = int(instructions[4].arg)
    step_5_add_x = int(instructions[5].arg)
    step_15_add_y = int(instructions[15].arg)

    x_extra = f'+ {-step_5_add_x}' if step_5_add_x < 0 else f'- {step_5_add_x}'
    z_div = 'z' if step_4_div_z == 1 else 'z // 26'
    z_times_26 = 'z * 26' if step_4_div_z == 1 else 'z'

    print(f'{index:2d}) div z {step_4_div_z} ; add y {step_15_add_y} ; add x {step_5_add_x}')
    print(f'{index:2d}) x = z % 26 == w {x_extra}')  # ? 0 : 1
    if step_4_div_z == 1:
        print(f'{index:2d})  x != w: z_out = {z_times_26} + w + {step_15_add_y}')
    else:
        print(f'{index:2d})  x == w: z_out = {z_div}')
    print()


def check_model_number(groups: List[List[Instruction]], seed):
    Input.seed = seed
    values = dict(x=0, y=0, z=0)
    for group_index, group in enumerate(groups):
        for instruction in group:
            instruction.evaluate(values)
    return values['z'] == 0


def process(groups: List[List[Instruction]]):
    stack = list()
    values = ['0'] * 14

    # x = z0 % <step_4_div_z> + <step_5_add_x>
    # x = x == w ? 0 : 1
    # z = z0 // <step_4_div_z>
    # y = 25 * x + 1
    # z = z * y
    # y = x * (w + <step_15_add_y>)
    # z = z + y

    # inspired from explainers on Reddit
    #   and also by peeking at https://github.com/andrewmacheret/aoc/blob/master/2021/python/day24/main.py

    for group_index, instructions in enumerate(groups):
        step_4_div_z = int(instructions[4].arg)
        step_5_add_x = int(instructions[5].arg)
        step_15_add_y = int(instructions[15].arg)

        if step_4_div_z == 1:
            stack.insert(0, (group_index, step_15_add_y))
        else:
            from_group, value = stack.pop(0)
            extra = value + step_5_add_x
            if extra > 0:
                values[group_index] = '9'
                values[from_group] = str(9 - extra)
            else:
                values[group_index] = str(9 + extra)
                values[from_group] = '9'
            # print(f'{group_index:2d}) pop {value:2d} from {from_group:2d} -- w = z + {extra}')

    return ''.join(values)


if __name__ == '__main__':
    current_instructions = list()
    instruction_groups = list()

    for idx, line in enumerate(read_input().splitlines()):
        i = Instruction.parse(*line.split(' '))

        if i.operator == 'inp':
            if idx > 0:
                instruction_groups.append(current_instructions)
                current_instructions = list()

        current_instructions.append(i)
    else:
        instruction_groups.append(current_instructions)

    # for gi, group in enumerate(instruction_groups):
    #     print_formula(group, gi)

    result = process(instruction_groups)
    if check_model_number(instruction_groups, result):
        print('result:', result)

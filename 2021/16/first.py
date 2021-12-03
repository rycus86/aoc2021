def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


def four_digit_binary(hex_digit):
    value = bin(int(hex_digit, 16))[2:]
    while len(value) < 4:
        value = '0' + value
    return value


class Packet(object):
    def __init__(self, bits):
        self.bits = bits
        self.version = int(bits[0:3], 2)
        self.type_id = int(bits[3:6], 2)
        self.remainder = bits[6:]

    def details(self):
        return dict(cls=self.__class__.__name__,
                    version=self.version,
                    type=self.type_id)

    def part_one(self):
        return self.version

    @classmethod
    def parse(cls, bits):
        if Packet(bits).type_id == 4:
            return Literal(bits)
        else:
            return Operator(bits).transform()


class Literal(Packet):
    def __init__(self, bits):
        super().__init__(bits)

        groups = ''
        value_len = 0

        while self.remainder:
            prefix, group, self.remainder = self.remainder[0], self.remainder[1:5], self.remainder[5:]
            groups += group
            value_len += 1 + len(group)
            if prefix == '0':
                break

        self.value = int(groups, 2)

        # 6 for the header bits
        self.packet_length = value_len + 6

    def details(self):
        result = dict(super(Literal, self).details())
        result.update(dict(value=self.value))
        return result


class Operator(Packet):
    def __init__(self, bits):
        super().__init__(bits)

        self.length_type_id = int(self.remainder[0], 2)
        self.children = list()

    def details(self):
        result = dict(super(Operator, self).details())
        result.update(dict(length_type=self.length_type_id,
                           children=list(p.details() for p in self.children)))
        return result

    def transform(self):
        if self.length_type_id == 0:
            return OperatorWithTotalLength(self.bits)
        elif self.length_type_id == 1:
            return OperatorWithSubPackets(self.bits)
        else:
            raise Exception(f'Invalid length type ID: {self.length_type_id}')

    def part_one(self):
        return self.version + sum(c.part_one() for c in self.children)


class OperatorWithTotalLength(Operator):
    def __init__(self, bits):
        super().__init__(bits)

        self.total_length = int(self.remainder[1:16], 2)
        child_packets = self.remainder[16:16+self.total_length]

        # 6 for header + 1 for length type + 15 length
        self.packet_length = self.total_length + 6 + 1 + 15

        while child_packets:
            packet = Packet.parse(child_packets)
            self.children.append(packet)
            child_packets = child_packets[packet.packet_length:]

    def details(self):
        result = dict(super().details())
        result.update(dict(total_length=self.total_length))
        return result


class OperatorWithSubPackets(Operator):
    def __init__(self, bits):
        super().__init__(bits)

        self.number_of_children = int(self.remainder[1:12], 2)
        child_packets = self.remainder[12:]

        total_length = 0

        for _ in range(self.number_of_children):
            packet = Packet.parse(child_packets)
            self.children.append(packet)
            child_packets = child_packets[packet.packet_length:]
            total_length += packet.packet_length

        # 6 for header + 1 for length type + 11 number of children + children length
        self.packet_length = total_length + 6 + 1 + 11

    def details(self):
        result = dict(super().details())
        result.update(dict(num_children=self.number_of_children))
        return result


if __name__ == '__main__':
    line = read_input().strip()
    source = ''.join(four_digit_binary(x) for x in line)

    # import json
    # print('debug:', json.dumps(Packet.parse(source).details(), indent=2))
    print('result:', Packet.parse(source).part_one())

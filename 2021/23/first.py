def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


hallway_stops = (1, 2, 4, 6, 8, 10, 11)
room_stops = (3, 5, 7, 9)
min_energy = 10 ** 6

state_visited = set()


class Amphipod(object):
    def __init__(self, type, x, y, moved=0, move_count=0, previous_positions=None, _step_cost=None, _preferred_room=None):
        self.type = type
        self.x = x
        self.y = y
        self.moved = moved
        self.move_count = move_count
        self.previous_positions = previous_positions or set()

        self.step_cost = _step_cost or self._step_cost()
        self.preferred_room = _preferred_room or self._preferred_room()

        self.total_cost = self.step_cost * self.moved

    def _step_cost(self):
        if self.type == 'A':
            return 1
        elif self.type == 'B':
            return 10
        elif self.type == 'C':
            return 100
        elif self.type == 'D':
            return 1000

    def move_to(self, x):
        if self.y > 1:  # not in hallway
            self.moved += abs(self.y - 1)
            self.y = 1

        self.moved += abs(self.x - x)
        self.move_count += 1
        self.x = x

        self.total_cost = self.step_cost * self.moved
        self.previous_positions.add(self.x)

    def drop_to(self, y):
        self.moved += abs(self.y - y)
        self.y = y

        self.total_cost = self.step_cost * self.moved
        self.previous_positions.add(self.x)

    def has_visited(self, x, y):
        return x in self.previous_positions

    def _preferred_room(self):
        if self.type == 'A':
            return 3
        elif self.type == 'B':
            return 5
        elif self.type == 'C':
            return 7
        elif self.type == 'D':
            return 9

    def copy(self):
        return Amphipod(self.type, self.x, self.y, self.moved, self.move_count,
                        self.previous_positions, self.step_cost, self.preferred_room)

    def __repr__(self):
        return f'{self.type}({self.x}x{self.y})'


def find_partner(all_amphipods, a):
    for p in all_amphipods:
        if p.type == a.type:
            if p.x != a.x or p.y != a.y:
                return p


def needs_to_move(all_amphipods, a):
    if a.x != a.preferred_room:
        return True  # we are not in our room

    # otherwise we are in the right room
    if a.y == 3:
        return False  # we are on the bottom, stay

    for p in all_amphipods:
        if p.x == a.x and p.y == 3:
            # only move if there is another type below us
            return p.type != a.type


def can_move(all_amphipods, a):
    if a.y <= 2:
        return True

    if a.y == 3:
        if a.x == a.preferred_room:
            return False  # already at the right place

        if not any(p.y == 2 and p.x == a.x for p in all_amphipods):
            return True


def is_available_to_pair(all_amphipods, a):
    if a.y < 3:
        return False  # not at the bottom

    if any(p.y == 2 and p.x == a.x for p in all_amphipods):
        return False  # someone else is blocking the entrance

    return True  # all clear


def is_hallway_free(all_amphipods_x, from_x, to_x):
    in_hallway = all_amphipods_x
    if not in_hallway:
        return True

    step = 1 if from_x < to_x else -1
    for x in range(from_x + step, to_x + step, step):
        if x in in_hallway:
            return False

    return True


def is_room_free_for(all_amphipods, a):
    return bottom_pos_at(all_amphipods, a.preferred_room) == 3


def bottom_pos_at(all_amphipods, x):
    if x in hallway_stops:
        return 1
    elif any(p.x == x and p.y == 2 for p in all_amphipods):
        return 1
    elif any(p.x == x and p.y == 3 for p in all_amphipods):
        return 2
    else:
        return 3


def total_score(all_amphipods):
    return sum(a.total_cost for a in all_amphipods)


def is_finished(all_amphipods):
    return all(not needs_to_move(all_amphipods, a) for a in all_amphipods)


def advance(all_amphipods, next_amphipod, target_x, drop_to_bottom=False, resume=True):
    a = all_amphipods[next_amphipod]

    all_amphipods.remove(a)

    a.move_to(target_x)
    if drop_to_bottom:
        bottom = bottom_pos_at(all_amphipods, target_x)
        a.drop_to(bottom)

    all_amphipods.append(a)

    total = total_score(all_amphipods)

    visit_key = '+'.join(sorted(map(str, all_amphipods))) + '--' + str(total)
    if visit_key in state_visited:
        return
    else:
        state_visited.add(visit_key)

    global min_energy

    if total >= min_energy:
        return

    if is_finished(all_amphipods):
        min_energy = total
        print('=> winner:', total, all_amphipods)
        return

    # assume less than 10 steps
    if a.move_count > 10:
        print('too many steps:', a, a.move_count)
        return

    for idx, amphipod in enumerate(all_amphipods):
        if needs_to_move(all_amphipods, amphipod) and can_move(all_amphipods, amphipod):
            hallway_amphipod_x = set(a.x for a in all_amphipods if a.y == 1)

            if is_room_free_for(all_amphipods, amphipod) and is_hallway_free(hallway_amphipod_x, amphipod.x, amphipod.preferred_room):
                positions_copy = [c.copy() for c in all_amphipods]
                advance(positions_copy, idx, amphipod.preferred_room, drop_to_bottom=True, resume=resume)
                return

            buddy = find_partner(all_amphipods, amphipod)
            if is_available_to_pair(all_amphipods, buddy) and is_hallway_free(hallway_amphipod_x, amphipod.x, buddy.x):
                positions_copy = [c.copy() for c in all_amphipods]
                advance(positions_copy, idx, buddy.x, drop_to_bottom=True, resume=resume)
                return

            # we should move into the hallway
            for target in hallway_stops:
                if not amphipod.has_visited(target, 1) and is_hallway_free(hallway_amphipod_x, amphipod.x, target):
                    positions_copy = [c.copy() for c in all_amphipods]
                    advance(positions_copy, idx, target, resume=resume)


def get_position_map(all_amphipods):
    area = '''
#############
#...........#
###.#.#.#.###
  #.#.#.#.#
  #########
'''.strip().splitlines()

    for a in all_amphipods:
        current = area[a.y]
        current = current[:a.x] + a.type + current[a.x+1:]
        area[a.y] = current

    contents = ''

    for line in area:
        contents += line + '\n'

    contents += f'{all_amphipods} {total_score(all_amphipods)}'

    return contents


def print_positions(all_amphipods):
    print(get_position_map(all_amphipods))


if __name__ == '__main__':
    positions = list()

    for li, line in enumerate(read_input().splitlines()):
        for idx, item in enumerate(line):
            if 'A' <= item <= 'D':
                positions.append(Amphipod(item, idx, li))

    for idx, amphipod in enumerate(positions):
        if needs_to_move(positions, amphipod) and can_move(positions, amphipod):
            for target in hallway_stops:
                positions_copy = [c.copy() for c in positions]
                advance(positions_copy, idx, target)

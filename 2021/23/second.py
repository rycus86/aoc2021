from typing import List, Iterable, Dict


def read_input():
    with open('input.txt', 'r') as input_file:
        return input_file.read()


costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}
target_rooms = {
    'A': 3,
    'B': 5,
    'C': 7,
    'D': 9
}

room_depth = 4
hallway_stops = (6, 4, 8, 2, 10, 1, 11)
room_stops = (3, 5, 7, 9)
min_score = 10 ** 10


class Amphipod(object):
    def __init__(self, type: str, x: int, y: int, moved=0):
        self.type = type
        self.x = x
        self.y = y
        self.moved = moved
        self.step_cost = costs[self.type]
        self.preferred_room = target_rooms[self.type]

        self.total_cost = self.step_cost * self.moved

    def move_to(self, x):
        self.moved += abs(self.x - x) + abs(self.y - 1)
        self.total_cost = self.step_cost * self.moved

        self.x = x
        self.y = 1

    def sinx(self, y_distance):
        self.moved += y_distance
        self.total_cost = self.step_cost * self.moved

        self.y += y_distance

    def copy(self):
        return Amphipod(self.type, self.x, self.y, self.moved)

    def __lt__(self, other):
        return self.type > other.type

    def __repr__(self):
        return f'{self.type}({self.x}x{self.y})'


class Room(list):
    def __init__(self, x, type, children: List[Amphipod] = None, pruned: List[Amphipod] = None):
        super().__init__()
        self.x = x
        self.type = type
        self.pruned = pruned or list()
        if children:
            self.extend(children)

    def prune(self):
        while len(self) and self[-1].type == self.type:
            self.pruned.append(self.pop(-1))

    def peek(self) -> Amphipod:
        return self[0]

    def take(self) -> Amphipod:
        return self.pop(0)

    def enter(self, child):
        depth = self.entry_depth()
        child.sinx(depth)
        self.pruned.append(child)

    def entry_depth(self):
        return room_depth - len(self.pruned)

    def is_empty(self) -> bool:
        return len(self) == 0

    def is_finished(self) -> bool:
        return len(self.pruned) == room_depth

    def score(self):
        return sum(child.total_cost for child in self.pruned)

    def copy(self):
        return Room(self.x, self.type,
                    [child.copy() for child in self],
                    [child.copy() for child in self.pruned])


class Hallway(dict):
    def __init__(self, children: Dict[int, Amphipod] = None):
        super().__init__()
        if children:
            self.update(children)
        else:
            self.update({x: None for x in hallway_stops})

    def move(self, child, position):
        child.move_to(position)
        self[position] = child

    def iter_members(self) -> Iterable[Amphipod]:
        for child in self.values():
            if child is not None:
                yield child

    def take_child(self, pos: int) -> Amphipod:
        taken, self[pos] = self[pos], None
        return taken

    def iter_available_targets(self, amphipod: Amphipod):
        for x in hallway_stops:
            if self.can_move_to(amphipod, x):
                yield x

    def can_move_to(self, amphipod: Amphipod, target: int):
        step = 1 if target > amphipod.x else -1
        x = amphipod.x
        while x != target:
            x += step
            if x not in hallway_stops:
                continue
            if self[x] is not None:
                return False
        return True

    def is_empty(self) -> bool:
        return all(child is None for child in self.values())

    def duplicate(self):
        return Hallway({pos: self._copy_at(pos) for pos in hallway_stops})

    def _copy_at(self, pos) -> Amphipod:
        original = self[pos]  # type: Amphipod
        if original:
            return original.copy()

    def score_hint(self):
        return sum(child.total_cost for child in self.values() if child is not None)


def get_position_map(rooms: Dict[str, Room], hallway: Hallway):
    area = '''
#############
#...........#
###.#.#.#.###
'''

    for _ in range(room_depth - 1):
        area += '  #.#.#.#.#\n'

    area += '  #########'
    area = area.strip().splitlines()

    total_score = hallway.score_hint()
    all_children = list()

    for room in rooms.values():
        all_children.extend(room)
        all_children.extend(room.pruned)
        total_score += room.score()

    all_children.extend(hallway.iter_members())

    for a in all_children:
        current = area[a.y]
        current = current[:a.x] + a.type + current[a.x + 1:]
        area[a.y] = current

    contents = ''

    for line in area:
        contents += line + '\n'

    contents = contents.strip() + f'#### score={total_score}'

    return contents


def print_positions(rooms: Dict[str, Room], hallway: Hallway):
    print(get_position_map(rooms, hallway))
    print()


def advance(rooms: Dict[str, Room], hallway: Hallway):
    global min_score

    total = sum(room.score() for room in rooms.values())

    if hallway.is_empty() and all(room.is_empty() for room in rooms.values()):
        # we're done, check the score
        if total < min_score:
            min_score = total
            print('min. score:', min_score)
            # print_positions(rooms, hallway)
            return True

    if total >= min_score:
        # we already found a better way
        return

    # check if we can move them off the hallway
    for child in hallway.iter_members():
        room = rooms[child.type]
        if room.is_empty():
            if hallway.can_move_to(child, child.preferred_room):
                copy_hallway = hallway.duplicate()  # type: Hallway
                copy_rooms = {rt: rm.copy() for rt, rm in rooms.items()}  # type: Dict[str, Room]
                copy_child = copy_hallway[child.x]

                copy_hallway.take_child(copy_child.x)  # remove from hallway
                copy_child.move_to(child.preferred_room)  # move above room
                copy_rooms[room.type].enter(copy_child)  # move into the room

                # start a new loop for our next moves
                advance(copy_rooms, copy_hallway)
                return

    # check if we should move them out of their rooms
    for room in rooms.values():
        if room.is_empty():
            continue

        child = room.peek()

        if rooms[child.type].is_empty() and hallway.can_move_to(child, child.preferred_room):
            copy_rooms = {rt: rm.copy() for rt, rm in rooms.items()}  # type: Dict[str, Room]

            # take from the room
            copy_child = copy_rooms[room.type].take()  # type: Amphipod
            # move above target room
            copy_child.move_to(rooms[child.type].x)
            # enter room
            copy_rooms[child.type].enter(copy_child)

            # start a new loop for our next moves
            advance(copy_rooms, hallway.duplicate())
            return

        for target_x in hallway.iter_available_targets(child):
            copy_hallway = hallway.duplicate()  # type: Hallway
            copy_rooms = {rt: rm.copy() for rt, rm in rooms.items()}  # type: Dict[str, Room]

            # take from the room
            copy_child = copy_rooms[room.type].take()  # type: Amphipod
            # move to the hallway
            copy_hallway.move(copy_child, target_x)

            advance(copy_rooms, copy_hallway)


if __name__ == '__main__':
    all_rooms = {x: Room(x, t) for t, x in target_rooms.items()}
    the_hallway = Hallway()

    full_input = read_input().splitlines()
    full_input = full_input[0:3] + ['  #D#C#B#A#', '  #D#B#A#C#'] + full_input[3:]
    # room_depth = 2  # for debugging

    for li, line in enumerate(full_input):
        for idx, item in enumerate(line):
            if 'A' <= item <= 'D':
                all_rooms[idx].append(Amphipod(item, idx, li))

    rooms_by_type = dict()
    for a_room in all_rooms.values():
        a_room.prune()
        rooms_by_type[a_room.type] = a_room

    # print_positions(rooms_by_type, the_hallway)

    advance(rooms_by_type, the_hallway)

from shared.utils import *


class Directory(object):
    directories: Dict[str, Any]
    files: Dict[str, int]

    def __init__(self, parent, path):
        self.parent = parent
        self.path = path
        self.directories = dict()
        self.files = dict()

    @property
    def full_path(self):
        if self.parent:
            if self.parent.path == '/':
                return f'/{self.path}'
            else:
                return f'/{self.parent.path}/{self.path}'
        else:
            return self.path

    def move_in(self, child):
        if child in self.directories:
            return self.directories[child]
        else:
            created = Directory(self, child)
            self.directories[child] = created
            return created

    def move_out(self):
        return self.parent

    def sum_size(self):
        sum_directories = sum(ch.sum_size() for ch in self.directories.values())
        return sum_directories + sum(self.files.values())

    def walk_directories(self):
        yield self
        for child in self.directories.values():
            for chw in child.walk_directories():
                yield chw

    def __repr__(self):
        return f'Dir({self.full_path} = {self.sum_size()})'


class Day07(Solution):
    root_directory: Directory

    def setup(self):
        self.root_directory = Directory(None, '/')
        current_directory = self.root_directory
        in_listing = False

        for line in self.input_lines():
            if line.startswith('$ cd '):
                in_listing = False

                if line == '$ cd ..':
                    current_directory = current_directory.move_out()
                elif line == '$ cd /':
                    current_directory = self.root_directory
                else:
                    child = line.replace('$ cd ', '')
                    current_directory = current_directory.move_in(child)

            elif line == '$ ls':
                in_listing = True

            elif in_listing:
                if line.startswith('dir '):
                    child = line.replace('dir ', '')
                    current_directory.move_in(child)
                else:
                    size, name = line.split()
                    current_directory.files[name] = int(size)

    def part_1(self):
        for directory in self.root_directory.walk_directories():
            size = directory.sum_size()
            if size <= 100000:
                self.add_result(size)

    def part_2(self):
        total_space = 70000000
        needed_space = 30000000 - (total_space - self.root_directory.sum_size())

        candidates = list()

        for directory in self.root_directory.walk_directories():
            size = directory.sum_size()
            if size > needed_space:
                candidates.append((size, directory))

        return next(iter(sorted(candidates)))[0]


Day07(__file__).solve()

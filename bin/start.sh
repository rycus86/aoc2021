#!/bin/sh

if [ -z "$1" ]; then
    echo "No day given"
    exit 1
fi

if [ -f "2024/$1/main.py" ]; then
    echo "Python code for this day already exists"
    exit 1
fi

mkdir -p "2024/$1"

touch "2024/$1/input.txt"
cat << EOF > "2024/$1/main.py"
from shared.utils import *


class Day$1(Solution):

    def setup(self):
        pass

    def part_1(self):
        return 'TODO'

    def part_2(self):
        pass


Day$1(__file__).solve()
EOF

idea "2024/$1/input.txt"
idea "2024/$1/main.py"

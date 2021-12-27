from shared.utils import *


class Day23(Solution):
    cups: List[int]

    def setup(self):
        self.cups = list(map(int, '643719258'))

    def part_1(self):
        current = 0

        for _ in range(100):
            # rotate the current one to the front
            self.cups = self.cups[current:] + self.cups[0:current]
            # pick up the three cups
            selected, floating = self.cups[0], self.cups[1:4]
            # remove the three cups
            self.cups = [self.cups[0]] + self.cups[4:]

            # find destination
            destination_index = -1
            target = selected - 1
            while destination_index < 0:
                if target in self.cups:
                    destination_index = self.cups.index(target)
                else:
                    target -= 1
                    if target <= 0:
                        target = 9

            # insert the three floating cups
            self.cups[destination_index:destination_index + 1] = [self.cups[destination_index]] + floating

            # select new current
            current = self.cups.index(selected) + 1
            if current >= len(self.cups):
                current = 0

        idx_one = self.cups.index(1)
        return ''.join(map(str, self.cups[idx_one + 1:] + self.cups[:idx_one]))

    def part_2(self):
        # based on some explainers on Reddit

        # add the rest of the numbers up to 1 million
        updated = self.cups + list(range(10, 1000000 + 1))
        # dict from <value> to the <next-value>
        follower = {value: updated[(idx + 1) % 1000000] for idx, value in enumerate(updated)}

        # start with the first cup in the input list
        current = updated[0]

        for _ in range(10000000):
            # get the three cups after current
            cup1 = follower[current]
            cup2 = follower[cup1]
            cup3 = follower[cup2]

            # current will now be followed by the cup after the three cups
            follower[current] = follower[cup3]

            # compute target
            floating = {cup1, cup2, cup3}
            target = current - 1
            while target in floating or target < 1:
                if target < 1:
                    target = 1000000
                else:
                    target -= 1

            # the third cup is followed by the cup after the destination cup
            follower[cup3] = follower[target]
            # destination will be followed by the three cups
            follower[target] = cup1

            # move on to the next current
            current = follower[current]

        # take the two cups after cup 1
        a = follower[1]
        b = follower[a]

        return a * b


Day23().solve()

from shared.utils import *


class Day06(Solution):
    def part_1(self):
        for group in self.input.split('\n\n'):
            group_answers = set()

            for answers in group.split('\n'):
                group_answers.update(answers)

            self.add_result(len(group_answers))

    def part_2(self):
        for group in self.input.split('\n\n'):
            group_answers = None

            for answers in group.split('\n'):
                if group_answers is None:
                    group_answers = set(answers)
                else:
                    group_answers.intersection_update(answers)

            self.add_result(len(group_answers))


Day06(__file__).solve()

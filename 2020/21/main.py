import re
from collections import defaultdict

from shared.utils import *


class Day21(Solution):
    meals: List[Tuple[List, List]]
    options: Dict[str, Set]
    all_ingredients: Set
    no_allergens: Set

    def setup(self):
        pattern = re.compile(r'([a-z ]+) \(contains ([a-z, ]+)\)')

        self.meals = list()
        for line in self.input_lines():
            ingredients, allergens = pattern.match(line).groups()
            self.meals.append((ingredients.split(' '), allergens.split(', ')))

        self.all_ingredients = set()
        self.options = defaultdict(set)

        for ingredients, allergens in self.meals:
            self.all_ingredients.update(ingredients)

            for allergen in allergens:
                self.options[allergen].update(ingredients)

        for ingredients, allergens in self.meals:
            for allergen in allergens:
                self.options[allergen].intersection_update(ingredients)

        self.no_allergens = set(self.all_ingredients)
        for ingredients in self.options.values():
            for ingredient in ingredients:
                if ingredient in self.no_allergens:
                    self.no_allergens.remove(ingredient)

    def part_1(self):
        for ingredients, _ in self.meals:
            for ingredient in self.no_allergens:
                self.add_result(ingredients.count(ingredient))

    def part_2(self):
        mapping = dict()

        while len(mapping) < len(self.options):
            for allergen, ingredients in self.options.items():
                unmapped = set(ingredient for ingredient in ingredients if ingredient not in mapping.values())
                if len(unmapped) == 1:
                    mapping[allergen] = unmapped.pop()

        result = list()
        for allergen, ingredient in sorted(mapping.items()):
            result.append(ingredient)

        return ','.join(result)


Day21(__file__).solve()

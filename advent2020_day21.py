from utils import read_data
from typing import Dict, Set, Tuple, List
from collections import defaultdict


def part_one(data: List[str]) -> Tuple[Dict[str, Set[str]], int]:
    allergens_dict: Dict[str, Set[str]] = {}
    ingredient_counts = defaultdict(int)
    for line in data:
        ingredients_raw, allergens_raw = line.split(" (contains ")

        ingredients = ingredients_raw.split(" ")
        for ingredient in ingredients:
            ingredient_counts[ingredient] += 1

        # Strip off the final ) from the contains list
        allergens_raw = allergens_raw[:-1]
        allergens = allergens_raw.split(", ")
        for allergen in allergens:
            if allergen in allergens_dict:
                allergens_dict[allergen] = allergens_dict[allergen].intersection(ingredients)
            else:
                allergens_dict[allergen] = set(ingredients)
    allergy_ingredients = set().union(*allergens_dict.values())
    no_allergy_ingredients = set(ingredient_counts.keys()) - allergy_ingredients
    return allergens_dict, sum(ingredient_counts[x] for x in no_allergy_ingredients)


def part_two(allergens_dict: Dict[str, Set[str]]) -> str:
    canonical_allergens_dict = {}
    while allergens_dict:
        known_items = [x for x in allergens_dict.items() if len(x[1]) == 1]
        for allergen, ingredient_set in known_items:
            canonical_allergens_dict[allergen] = ingredient_set.pop()
            allergens_dict.pop(allergen)
            for ingredient_set in allergens_dict.values():
                ingredient_set.discard(canonical_allergens_dict[allergen])
    return ",".join(canonical_allergens_dict[x] for x in sorted(canonical_allergens_dict.keys()))


def main():
    food_list = read_data().split("\n")
    allergens, part_one_solution = part_one(food_list)
    print(f"Part one: {part_one_solution}")
    print(f"Part two: {part_two(allergens)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

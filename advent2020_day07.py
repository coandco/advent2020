from utils import read_data
from typing import Dict, List, Set
import re

LINE_REGEX = re.compile(r'(?P<color>[a-z]+ [a-z]+) bags contain (?P<contain>[^.]*).')
CONTAINS_REGEX = re.compile(r'(?P<num>\d+) (?P<color>[a-z]+ [a-z]+) bags?')


class Bag:
    def __init__(self, line: str):
        self.contains = {}
        self.bag_value = 0
        match = LINE_REGEX.match(line)
        if match:
            self.color, contains_list = match.groups()
            contains_list = match.group('contain').split(", ")
            for item in contains_list:
                if item == "no other bags":
                    self.bag_value = 0
                else:
                    match = CONTAINS_REGEX.match(item)
                    if match:
                        num, color = match.groups()
                        self.contains[color] = int(num)
                    else:
                        raise Exception(f"Failed to match contains regex on {item}")

        else:
            raise Exception(f"Couldn't parse line: {line}")
        self.unknown_contains = self.contains.copy()


def build_reversed_bags_hash(bags_hash: Dict[str, Bag]) -> Dict[str, List[str]]:
    reversed_bags_hash = {}
    for color in bags_hash.keys():
        reversed_bags_hash[color] = [x.color for x in bags_hash.values() if color in x.contains.keys()]
    return reversed_bags_hash


def get_all_containing_bags(reversed_bags_hash: Dict[str, List[str]], to_find: str) -> Set[str]:
    current_set = {to_find}
    while True:
        start_set = current_set.copy()
        for color in start_set:
            current_set.update(reversed_bags_hash[color])
        if start_set == current_set:
            return current_set - {to_find}


def generate_bag_values(bags_hash: Dict[str, Bag], reversed_bags_hash: Dict[str, List[str]]) -> Dict[str, int]:
    known_bag_values = {x.color: x.bag_value for x in bags_hash.values() if len(x.unknown_contains) == 0}
    while True:
        this_pass = list(known_bag_values.keys())
        for color in this_pass:
            for parent_color in reversed_bags_hash[color]:
                if parent_color in known_bag_values:
                    continue
                parent_bag = bags_hash[parent_color]
                if color in parent_bag.unknown_contains.keys():
                    # Add the known value times the number it contains
                    parent_bag.bag_value += (
                                parent_bag.contains[color] + (known_bag_values[color] * parent_bag.contains[color]))
                    parent_bag.unknown_contains.pop(color)
                    # If we've fully determined the value of the bag, add it to the known list
                    if len(parent_bag.unknown_contains) == 0:
                        known_bag_values[parent_bag.color] = parent_bag.bag_value
        if len(known_bag_values) == len(this_pass):
            break
    return known_bag_values


def main():
    bags = [Bag(x) for x in read_data().splitlines()]
    bags_hash = {x.color: x for x in bags}
    reversed_bags_hash = build_reversed_bags_hash(bags_hash)
    part_one_bags = get_all_containing_bags(reversed_bags_hash, 'shiny gold')

    print(f"Part one: {len(part_one_bags)}")

    known_bag_values = generate_bag_values(bags_hash, reversed_bags_hash)
    print(f"Part 2: {known_bag_values['shiny gold']}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

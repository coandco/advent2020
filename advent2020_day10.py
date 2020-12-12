from utils import read_data
from typing import List, Dict


def part_one(data: List[int]) -> int:
    # Add the wall socket and your device to the list
    full_data = [0] + sorted(data) + [max(data) + 3]
    # Calculate the difference between each item
    differences = [j - i for i, j in zip(full_data[:-1], full_data[1:])]
    return differences.count(1) * differences.count(3)


def calculate_value(known_cache: Dict[int, int], entry: int) -> int:
    total = 0
    for step in (1, 2, 3):
        # If value + step is in the cache, add it to your own value
        total += known_cache.get(entry + step, 0)
    # Add this calculated value to the cache before returning
    known_cache[entry] = total
    return total


def part_two(data: List[int]) -> int:
    # Add the wall socket and your device to the list
    full_data = [0] + sorted(data) + [max(data) + 3]
    # Start with our device and initialize the number of paths on it to one
    known_cache = {full_data[-1]: 1}
    # Go backwards through the list starting with the second-to-last item,
    # setting each item to the sum of the ones in range of it
    in_range = [calculate_value(known_cache, x) for x in reversed(full_data[:-1])]
    # Finally, return the calculated value for your wall socket,
    # which will now be at the end of the list because of the reversal
    return in_range[-1]


if __name__ == '__main__':
    INPUT = [int(x) for x in read_data().split("\n")]
    print(f"Part one: {part_one(INPUT)}")
    print(f"Part two: {part_two(INPUT)}")

from utils import read_data
from itertools import combinations
from typing import List, Union


def find_invalid(data: List[int], preamble_length: int) -> Union[int, None]:
    known = data[:preamble_length]
    for item in data[preamble_length:]:
        item_valid = False
        for pair in combinations(known, 2):
            if sum(pair) == item:
                known.pop(0)
                known.append(item)
                item_valid = True
                break
        if item_valid:
            continue
        else:
            return item
    return None


def find_summed_range(data: List[int], target_number: int) -> List[int]:
    for i in range(len(data)):
        total = data[i]
        for j in range(i + 1, len(data)):
            total += data[j]
            if total == target_number:
                return data[i:j]
            elif total > target_number:
                break


if __name__ == '__main__':
    PREAMBLE_LENGTH = 25
    INPUT = [int(x) for x in read_data().split("\n")]

    invalid_entry = find_invalid(INPUT, PREAMBLE_LENGTH)
    print(f"First invalid entry: {invalid_entry}")

    good_range = find_summed_range(INPUT, invalid_entry)
    print(f"Min is {min(good_range)}, max is {max(good_range)}, sum is {min(good_range) + max(good_range)}")
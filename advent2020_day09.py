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


def main():
    preamble_length = 25
    lines = [int(x) for x in read_data().split("\n")]

    invalid_entry = find_invalid(lines, preamble_length)
    print(f"Part one: {invalid_entry}")

    good_range = find_summed_range(lines, invalid_entry)
    print(f"Part two: {min(good_range) + max(good_range)}")
    

if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

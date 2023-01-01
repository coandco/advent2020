import itertools
from utils import read_data
from typing import List
from math import prod


def sum_prod(num_list: List[int], sum_value: int, r_length: int) -> int:
    combinations = itertools.combinations(num_list, r_length)
    solution = [prod(x) for x in combinations if sum(x) == sum_value]
    return solution[0] if solution else None


def main():
    input_processed = [int(x) for x in read_data().split("\n")]
    print(f"Part one: {sum_prod(input_processed, 2020, 2)}")
    print(f"Part two: {sum_prod(input_processed, 2020, 3)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

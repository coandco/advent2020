from utils import read_data
from typing import List


def run_game(data: List[int], iterations: int) -> int:
    seen = {x: i for i, x in enumerate(data)}
    last_number = data[-1]
    for i in range(len(data), iterations):
        if last_number not in seen:
            new_last_number = 0
        else:
            new_last_number = (i-1) - seen[last_number]
        seen[last_number] = i-1
        last_number = new_last_number
    return last_number


def main():
    starting_numbers = [int(x) for x in read_data().split(",")]
    print(f"Part one: {run_game(starting_numbers, 2020)}")
    print(f"Part two: {run_game(starting_numbers, 30000000)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

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


INPUT = [int(x) for x in read_data().split(",")]
print(f"Part one answer: {run_game(INPUT, 2020)}")
print(f"Part two answer: {run_game(INPUT, 30000000)}")

import itertools
from utils import read_data
from math import prod


def sum_prod(num_list, sum_value, r_length):
    combinations = itertools.combinations(num_list, r_length)
    solution = [prod(x) for x in combinations if sum(x) == sum_value]
    return solution[0] if solution else None


if __name__ == '__main__':
    input_processed = [int(x) for x in read_data().split("\n")]
    print(sum_prod(input_processed, 2020, 2))
    print(sum_prod(input_processed, 2020, 3))

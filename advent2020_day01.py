import itertools
from utils import read_data

input_processed = [int(x) for x in read_data().split("\n")]

combinations = itertools.combinations(input_processed, 2)
sums = [(x[0] + x[1], x[0] * x[1]) for x in combinations if x[0] + x[1] == 2020]
print(sums[0][1])

threefold = list(itertools.combinations(input_processed, 3))
sums = [(x[0] + x[1] + x[2], x[0] * x[1] * x[2]) for x in threefold if x[0] + x[1] + x[2] == 2020]
print(sums[0][1])
from utils import read_data
from typing import List


def part_one(data: List[str]) -> int:
    mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    mem = {}
    for line in data:
        op, value = line.split(" = ")
        if op == "mask":
            mask = value
        else:
            address = int(op[4:-1])
            binary_value = f"{int(value):036b}"
            masked_value = "".join(binary_value[x] if mask[x] == "X" else mask[x] for x in range(len(binary_value)))
            mem[address] = int(masked_value, 2)
    return sum(mem.values())


def generate_possible_values(floating_binary: str):
    x_indices = [i for i, x in enumerate(floating_binary) if x == "X"]
    for i in range(0, pow(2, len(x_indices))):
        binary_replacements = f"{i:0b}".zfill(len(x_indices))
        result = list(floating_binary)
        for i, x in enumerate(x_indices):
            result[x] = binary_replacements[i]
        yield int("".join(result), 2)


def part_two(data: List[str]) -> int:
    mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    mem = {}
    for line in data:
        op, value = line.split(" = ")
        if op == "mask":
            mask = value
        else:
            binary_address = f"{int(op[4:-1]):036b}"
            masked_address = "".join(
                binary_address[x] if mask[x] == "0" else mask[x] for x in range(len(binary_address)))
            for address in generate_possible_values(masked_address):
                mem[address] = int(value)
    return sum(mem.values())


INPUT = read_data().split("\n")
print(f"Part one: {part_one(INPUT)}")
print(f"Part two: {part_two(INPUT)}")


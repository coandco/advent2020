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
            # Apply the mask by selecting the value for each position from one of the two strings,
            # depending on if it's an X or not
            masked_value = "".join(binary_value[x] if mask[x] == "X" else mask[x] for x in range(len(binary_value)))
            mem[address] = int(masked_value, 2)
    return sum(mem.values())


def generate_possible_values(floating_binary: str):
    # Find the index of each X in the input string
    x_indices = [i for i, x in enumerate(floating_binary) if x == "X"]
    # If we have 6 values, loop from 0 to 2^6 so we hit all combinations of 0 and 1 for them
    for i in range(0, pow(2, len(x_indices))):
        # Turn the i into a binary string with the same length as x_indices
        binary_replacements = f"{i:0b}".zfill(len(x_indices))
        # Convert the original string into a list so we can modify it
        result = list(floating_binary)
        for i, x in enumerate(x_indices):
            # Replace a single X in the floating binary with its replacement
            result[x] = binary_replacements[i]
        # Convert the result back to an int before we yield it
        yield int("".join(result), 2)


def part_two(data: List[str]) -> int:
    mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    mem = {}
    for line in data:
        op, value = line.split(" = ")
        if op == "mask":
            mask = value
        else:
            premask_address = int(op[4:-1])
            binary_address = f"{premask_address:036b}"
            # Only if the mask is a zero do we use the original.  Otherwise, we overwrite it with the mask.
            masked_address = "".join(binary_address[x] if mask[x] == "0" else mask[x]
                                     for x in range(len(binary_address)))

            for address in generate_possible_values(masked_address):
                mem[address] = int(value)
    return sum(mem.values())


def main():
    init_program = read_data().splitlines()
    print(f"Part one: {part_one(init_program)}")
    print(f"Part two: {part_two(init_program)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

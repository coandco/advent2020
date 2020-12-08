from utils import read_data
from typing import List


class Instruction:
    def __init__(self, opcode, arg):
        self.opcode = opcode
        self.arg = int(arg)

    def __repr__(self):
        return f"{self.opcode} {self.arg}"


INPUT = read_data().split("\n")


def run_program(data: List[Instruction], swap_number: int):
    pc = 0
    acc = 0
    seen_instructions = set()

    while True:
        current = data[pc]
        seen_instructions.add(pc)
        if current.opcode == "acc":
            acc += current.arg
            pc += 1
        elif (current.opcode == "jmp" and pc != swap_number) or (current.opcode == "nop" and pc == swap_number):
            pc += current.arg
        elif (current.opcode == "nop" and pc != swap_number) or (current.opcode == "jmp" and pc == swap_number):
            pc += 1
        if pc in seen_instructions:
            return True, acc
        if pc >= len(data):
            return False, acc

data = [Instruction(*x.split(" ")) for x in INPUT]

_, acc = run_program(data, -1)

print(f"Part one accumulator is {acc}")

current_swap = 0
while True:
    looped, acc = run_program(data, current_swap)
    if looped:
        # print(f"swapping instruction {current_swap} results in a loop")
        pass
    else:
        break
    current_swap += 1
print(f"After swapping instruction {current_swap} ({data[current_swap]}), the program exited normally with acc of {acc}")


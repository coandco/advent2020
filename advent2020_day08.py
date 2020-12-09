from utils import read_data
from typing import List, NamedTuple


class Instruction(NamedTuple):
    opcode: str
    arg: int

    @staticmethod
    def from_string(string):
        opcode, arg = string.split(" ")
        return Instruction(opcode, int(arg))

    def swap_opcode(self):
        if self.opcode == "jmp":
            return Instruction("nop", self.arg)
        elif self.opcode == "nop":
            return Instruction("jmp", self.arg)
        else:
            return self

    def __repr__(self):
        return f"{self.opcode} {self.arg}"


def run_program(data: List[Instruction]):
    pc = 0
    acc = 0
    seen_instructions = set()

    while True:
        current = data[pc]
        seen_instructions.add(pc)
        if current.opcode == "acc":
            acc += current.arg
            pc += 1
        elif current.opcode == "jmp":
            pc += current.arg
        elif current.opcode == "nop":
            pc += 1
        if pc in seen_instructions:
            return True, acc
        if pc >= len(data):
            return False, acc


INPUT = read_data().split("\n")
data = [Instruction.from_string(x) for x in INPUT]

_, acc = run_program(data)

print(f"Part one accumulator is {acc}")

current_swap = 0
while True:
    modified_program = data[:]
    modified_program[current_swap] = modified_program[current_swap].swap_opcode()
    looped, acc = run_program(modified_program)
    if looped:
        # print(f"swapping instruction {current_swap} results in a loop")
        pass
    else:
        break
    current_swap += 1
print(f"After swapping instruction {current_swap} ({data[current_swap]}), the program exited normally with acc of {acc}")


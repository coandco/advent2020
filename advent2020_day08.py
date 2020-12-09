from utils import read_data
from typing import List, NamedTuple


class Instruction(NamedTuple):
    opcode: str
    arg: int

    @staticmethod
    def from_string(string):
        opcode, arg = string.split(" ")
        return Instruction(opcode, int(arg))

    def swap_opcode(self, opcode1, opcode2):
        if self.opcode == opcode1:
            return Instruction(opcode2, self.arg)
        elif self.opcode == opcode2:
            return Instruction(opcode1, self.arg)
        else:
            return self

    def __repr__(self):
        return f"{self.opcode} {self.arg}"


class ProgramResult(NamedTuple):
    acc: int
    looped: bool


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
            return ProgramResult(acc=acc, looped=True)
        if pc >= len(data):
            return ProgramResult(acc=acc, looped=False)


INPUT = read_data().split("\n")
data = [Instruction.from_string(x) for x in INPUT]

result = run_program(data)

print(f"Part one accumulator is {result.acc}")

current_swap = 0
while True:
    modified_program = data[:]
    modified_program[current_swap] = modified_program[current_swap].swap_opcode("jmp", "nop")
    result = run_program(modified_program)
    if result.looped:
        # print(f"swapping instruction {current_swap} results in a loop")
        pass
    else:
        break
    current_swap += 1
print(f"After swapping instruction {current_swap} ({data[current_swap]}), "
      f"the program exited normally with acc of {result.acc}")


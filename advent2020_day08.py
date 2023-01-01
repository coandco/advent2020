from utils import read_data
from typing import List, NamedTuple


class Instruction(NamedTuple):
    opcode: str
    arg: int

    @staticmethod
    def from_string(string: str) -> 'Instruction':
        opcode, arg = string.split(" ")
        return Instruction(opcode, int(arg))

    def swap_opcode(self, opcode1: str, opcode2: str) -> 'Instruction':
        if self.opcode == opcode1:
            return Instruction(opcode2, self.arg)
        elif self.opcode == opcode2:
            return Instruction(opcode1, self.arg)
        else:
            return self

    def __repr__(self) -> str:
        return f"{self.opcode} {self.arg}"


class ProgramResult(NamedTuple):
    acc: int
    looped: bool


def run_program(data: List[Instruction]) -> ProgramResult:
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


def main():
    parsed_data = [Instruction.from_string(x) for x in read_data().splitlines()]

    result = run_program(parsed_data)

    print(f"Part one: {result.acc}")

    current_swap = 0
    while True:
        modified_program = parsed_data[:]
        modified_program[current_swap] = modified_program[current_swap].swap_opcode("jmp", "nop")
        result = run_program(modified_program)
        if result.looped:
            # print(f"swapping instruction {current_swap} results in a loop")
            pass
        else:
            break
        current_swap += 1
    print(f"Part two: {result.acc}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

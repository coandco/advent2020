from utils import read_data
from typing import Optional, List, Tuple
from dataclasses import dataclass
from math import prod

@dataclass
class Node:
    value: int
    next: 'Node' = None
    prev: 'Node' = None
    dest: 'Node' = None

    def link_dest(self, max_node: 'Node'):
        if self.value == 1:
            self.dest = max_node
        else:
            current = self.prev
            while current is not self:
                if current.value == self.value - 1:
                    self.dest = current
                    return
                current = current.prev

    def __repr__(self):
        return f"Node(value={self.value})"


class CupCircle:
    def __init__(self):
        self.current: Optional[Node] = None
        self.max: Optional[Node] = None
        self.one_node: Optional[Node] = None
        self.length: int = 0

    @property
    def end(self):
        if self.current is None:
            return None
        return self.current.prev

    def append(self, value):
        self.length += 1
        new_node = Node(value=value)
        if self.current is None:
            new_node.next = new_node
            new_node.prev = new_node
            self.current = new_node
        else:
            new_node.next = self.end.next
            new_node.prev = self.end
            self.end.next = new_node
            self.current.prev = new_node
        if self.max is None or value > self.max.value:
            self.max = new_node
        if value == 1:
            self.one_node = new_node

    def link_all_dests(self):
        current = self.end
        while current.dest is None:
            current.link_dest(self.max)
            current = current.prev

    def rotate(self):
        assert self.current is not None, "Can't rotate an empty list"
        self.current = self.current.next

    def rotate_to_one(self):
        assert self.one_node is not None, "Can't rotate to the one if it doesn't exist"
        self.current = self.one_node

    def move_cups(self):
        assert self.length >= 4, "Can't pick up three cups from a list that's smaller than four"
        # First get references to the three-cup section
        first_cup = self.current.next
        third_cup = self.current.next.next.next
        # Second, excise the three-cup section from the list
        self.current.next = third_cup.next
        self.current.next.prev = self.current
        # Third, find the correct destination cup
        excised_values = (first_cup.value, first_cup.next.value, first_cup.next.next.value)
        dest_cup = self.current.dest
        while dest_cup.value in excised_values:
            dest_cup = dest_cup.dest
        # Fourth, link the three-cup section into the new location
        first_cup.prev = dest_cup
        third_cup.next = dest_cup.next
        # Finally, link the new location back into the three-cup section
        dest_cup.next.prev = third_cup
        dest_cup.next = first_cup

    def popleft(self):
        if self.length == 1:
            value = self.current.value
            self.current = None
        else:
            value = self.current.value
            old_current = self.current
            self.current = self.current.next
            self.current.prev = old_current.prev
            old_current.prev.next = self.current
        self.length -= 1
        if value == 1:
            self.one_node = None
        return value

    def values_after_one(self, num: int = 2) -> Tuple[int, int]:
        return self.one_node.next.value, self.one_node.next.next.value

    def as_list(self) -> List[int]:
        output = [self.current.value]
        temp = self.current.next
        while temp is not self.current:
            output.append(temp.value)
            temp = temp.next
        return output

    def __repr__(self):
        return self.as_list().__repr__()


def part_one(data: str, num_rounds: int) -> str:
    circle = CupCircle()
    for char in data:
        circle.append(int(char))
    circle.link_all_dests()

    for _ in range(num_rounds):
        circle.move_cups()
        circle.rotate()

    # Rotate to the one and remove it from the list
    circle.rotate_to_one()
    circle.popleft()

    output = ""
    while circle.length > 0:
        output += str(circle.popleft())
    return output


def part_two(data: str, length: int, num_rounds: int, debug: bool = False) -> int:
    if debug:
        print("Building list...")
    circle = CupCircle()
    for char in data:
        circle.append(int(char))
    for i in range(circle.max.value+1, length+1):
        if i % 100_000 == 0 and debug:
            print(f"Added {i} cups to the circle")
        circle.append(i)
    if debug:
        print("Linking cups...")
    circle.link_all_dests()

    if debug:
        print("Starting game...")
    for i in range(num_rounds):
        if i % 100_000 == 0 and debug:
            print(f"Completed {i} rounds, the numbers after one are {circle.values_after_one()}")

        circle.move_cups()
        circle.rotate()

    return prod(circle.values_after_one())


def main():
    part_one_answer = part_one(read_data(), 100)
    print(f"Part one: {part_one_answer}")
    part_two_answer = part_two(read_data(), 1_000_000, 10_000_000)
    print(f"Part two: {part_two_answer}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

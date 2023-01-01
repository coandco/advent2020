from utils import read_data
from typing import NamedTuple


class Coord(NamedTuple):
    y: int
    x: int

    def __add__(self, other) -> 'Coord':
        return Coord(y=self.y + other.y, x=self.x + other.x)

    @property
    def id(self) -> int:
        return (self.y * 8) + self.x

    @staticmethod
    def _bin_to_number(bin_string: str, limit: int, upper_char: str, lower_char: str) -> int:
        current_lower = 0
        current_upper = limit
        for char in bin_string:
            range_size = (current_upper - current_lower)
            if range_size <= 1:
                raise Exception("Tried to adjust sub-1")
            adjustment_size = int(range_size / 2)
            if char == upper_char:
                current_lower += adjustment_size
            elif char == lower_char:
                current_upper -= adjustment_size
        return current_upper - 1

    @staticmethod
    def from_seat(seat: str) -> 'Coord':
        return Coord(y=Coord._bin_to_number(seat[:7], 128, "B", "F"), x=Coord._bin_to_number(seat[-3:], 8, "R", "L"))


def main():
    seats = {Coord.from_seat(x) for x in read_data().split("\n")}
    highest_id = max(x.id for x in seats)
    print(f"Part one: {highest_id}")

    possible_seats = set()
    max_y = max(x.y for x in seats)
    min_y = min(x.y for x in seats)
    for i in range(min_y+1, max_y-1):
        for j in range(8):
            possible_seats.add(Coord(y=i, x=j))

    leftover_seats = possible_seats - seats
    if len(leftover_seats) == 1:
        (coord,) = leftover_seats
        print(f"Part two: {coord.id}")
    else:
        print(f"Part two ended up with {len(leftover_seats)} missing seats rather than one answer")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

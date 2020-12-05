from utils import read_data
from typing import NamedTuple


class Coord(NamedTuple):
    y: int
    x: int

    def __add__(self, other) -> 'Coord':
        return Coord(y=self.y + other.y, x=self.x + other.x)

    @property
    def id(self):
        return (self.y * 8) + self.x

    @staticmethod
    def _bin_to_number(bin_string, limit, upper_char, lower_char):
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
    def from_seat(seat: str):
        return Coord(y=Coord._bin_to_number(seat[:7], 128, "B", "F"), x=Coord._bin_to_number(seat[-3:], 8, "R", "L"))


highest_id = 0
max_y = 0
min_y = 9999
for line in read_data().split("\n"):
    coord = Coord.from_seat(line)
    if coord.id > highest_id:
        highest_id = coord.id
    if coord.y > max_y:
        max_y = coord.y
    if coord.y < min_y:
        min_y = coord.y

print(f"Part one: {highest_id}")

possible_seats = set()
for i in range(min_y+1, max_y-1):
    for j in range(8):
        possible_seats.add(Coord(y=i, x=j))

for line in read_data().split():
    possible_seats.discard(Coord.from_seat(line))

if len(possible_seats) == 1:
    (coord,) = possible_seats
    print(f"Part two: {coord.id}")
else:
    print(f"Part two ended up with {len(possible_seats)} missing seats rather than one answer")

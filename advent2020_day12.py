from utils import read_data
from typing import NamedTuple


class Coord(NamedTuple):
    y: int
    x: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(y=self.y + other.y, x=self.x + other.x)

    def __mul__(self, amount: int):
        return Coord(y=self.y*amount, x=self.x*amount)

    def __repr__(self):
        return f"Coord(y={self.y}, x={self.x})"

DIRECTIONS = {
    'N': Coord(y=-1, x=0),
    'E': Coord(y=0, x=1),
    'S': Coord(y=1, x=0),
    'W': Coord(y=0, x=-1)
}

RIGHT_TURN = {
    'N': 'E',
    'E': 'S',
    'S': 'W',
    'W': 'N'
}

LEFT_TURN = {
    'N': 'W',
    'E': 'N',
    'S': 'E',
    'W': 'S'
}


def move_direction(curpos: Coord, direction: str, amount: int):
    return curpos + (DIRECTIONS[direction] * amount)


def turn_right(current_heading: str, times: int):
    new_heading = current_heading
    for _ in range(times):
        new_heading = RIGHT_TURN[new_heading]
    return new_heading


def turn_left(current_heading: str, times: int):
    new_heading = current_heading
    for _ in range(times):
        new_heading = LEFT_TURN[new_heading]
    return new_heading


def rotate_right(point: Coord, times: int):
    new_point = point
    for _ in range(times):
        new_point = Coord(x=-new_point.y, y=new_point.x)
    return new_point


def rotate_left(point: Coord, times: int):
    new_point = point
    for _ in range(times):
        new_point = Coord(x=new_point.y, y=-new_point.x)
    return new_point


def part_one(data):
    current_loc = Coord(0, 0)
    current_heading = 'E'
    for line in data:
        if line[0] in DIRECTIONS.keys():
            current_loc = move_direction(current_loc, line[0], int(line[1:]))
        elif line[0] == 'R':
            num_turns = int(line[1:]) // 90
            current_heading = turn_right(current_heading, num_turns)
        elif line[0] == 'L':
            num_turns = int(line[1:]) // 90
            current_heading = turn_left(current_heading, num_turns)
        elif line[0] == 'F':
            current_loc = move_direction(current_loc, current_heading, int(line[1:]))
    return current_loc


def part_two(data):
    ship_loc = Coord(0, 0)
    waypoint_loc = Coord(y=-1, x=10)
    for line in data:
        if line[0] in DIRECTIONS.keys():
            waypoint_loc = move_direction(waypoint_loc, line[0], int(line[1:]))
        elif line[0] == 'R':
            num_rotations = int(line[1:]) // 90
            waypoint_loc = rotate_right(waypoint_loc, num_rotations)
        elif line[0] == 'L':
            num_rotations = int(line[1:]) // 90
            waypoint_loc = rotate_left(waypoint_loc, num_rotations)
        elif line[0] == 'F':
            ship_loc += (waypoint_loc * int(line[1:]))
    return ship_loc


INPUT = read_data().split("\n")

part_one_loc = part_one(INPUT)
print(f"Part one: the ship is at {part_one_loc}, a Manhattan distance of {abs(part_one_loc.x) + abs(part_one_loc.y)}")

part_two_loc = part_two(INPUT)
print(f"Part two: the ship is at {part_two_loc}, a Manhattan distance of {abs(part_two_loc.x) + abs(part_two_loc.y)}")


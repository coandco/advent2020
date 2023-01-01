from utils import read_data
from typing import NamedTuple, List


class Coord(NamedTuple):
    y: int
    x: int

    @property
    def manhattan_distance(self) -> int:
        return abs(self.x) + abs(self.y)

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(y=self.y + other.y, x=self.x + other.x)

    def __mul__(self, amount: int) -> 'Coord':
        return Coord(y=self.y*amount, x=self.x*amount)

    def __repr__(self) -> str:
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


def move_direction(curpos: Coord, direction: str, amount: int) -> Coord:
    return curpos + (DIRECTIONS[direction] * amount)


def turn_right(current_heading: str, times: int) -> str:
    new_heading = current_heading
    for _ in range(times):
        new_heading = RIGHT_TURN[new_heading]
    return new_heading


def turn_left(current_heading: str, times: int) -> str:
    new_heading = current_heading
    for _ in range(times):
        new_heading = LEFT_TURN[new_heading]
    return new_heading


def rotate_right(point: Coord, times: int) -> Coord:
    new_point = point
    for _ in range(times):
        new_point = Coord(x=-new_point.y, y=new_point.x)
    return new_point


def rotate_left(point: Coord, times: int) -> Coord:
    new_point = point
    for _ in range(times):
        new_point = Coord(x=new_point.y, y=-new_point.x)
    return new_point


def part_one(data: List[str]) -> Coord:
    current_loc = Coord(0, 0)
    current_heading = 'E'
    for line in data:
        op, value = line[0], int(line[1:])
        if op in DIRECTIONS.keys():
            current_loc = move_direction(current_loc, op, value)
        elif op == 'R':
            num_turns = (value // 90) % 4
            current_heading = turn_right(current_heading, num_turns)
        elif op == 'L':
            num_turns = (value // 90) % 4
            current_heading = turn_left(current_heading, num_turns)
        elif op == 'F':
            current_loc = move_direction(current_loc, current_heading, value)
    return current_loc


def part_two(data: List[str]) -> Coord:
    ship_loc = Coord(0, 0)
    waypoint_loc = Coord(y=-1, x=10)
    for line in data:
        op, value = line[0], int(line[1:])
        if op in DIRECTIONS.keys():
            waypoint_loc = move_direction(waypoint_loc, op, value)
        elif op == 'R':
            num_rotations = (value // 90) % 4
            waypoint_loc = rotate_right(waypoint_loc, num_rotations)
        elif op == 'L':
            num_rotations = (value // 90) % 4
            waypoint_loc = rotate_left(waypoint_loc, num_rotations)
        elif op == 'F':
            ship_loc += (waypoint_loc * value)
    return ship_loc


def main():
    instructions = read_data().splitlines()
    part_one_loc = part_one(instructions)
    print(f"Part one: {part_one_loc.manhattan_distance}")
    part_two_loc = part_two(instructions)
    print(f"Part two: {part_two_loc.manhattan_distance}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

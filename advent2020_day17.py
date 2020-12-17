from utils import read_data
from typing import NamedTuple, List, Set


class Coord3D(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other: 'Coord3D') -> 'Coord3D':
        return Coord3D(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def __repr__(self) -> str:
        return f"Coord(x={self.x}, y={self.y}, z={self.z})"


class Coord4D(NamedTuple):
    x: int
    y: int
    z: int
    w: int

    def __add__(self, other: 'Coord4D') -> 'Coord4D':
        return Coord4D(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z, w=self.w + other.w)

    def __repr__(self) -> str:
        return f"Coord(x={self.x}, y={self.y}, z={self.z}, w={self.w})"


NEIGHBORS_3D = [Coord3D(x, y, z) for x in range(-1, 2) for y in range(-1, 2) for z in range(-1, 2)
                if (x, y, z) != (0, 0, 0)]

NEIGHBORS_4D = [Coord4D(x, y, z, w) for x in range(-1, 2) for y in range(-1, 2) for z in range(-1, 2) for w in range(-1, 2)
                if (x, y, z, w) != (0, 0, 0, 0)]


def input_to_3d_points(data: List[str]) -> Set[Coord3D]:
    active_cubes = set()
    for i, line in enumerate(data):
        for j, char in enumerate(line):
            if char == "#":
                active_cubes.add(Coord3D(x=j, y=i, z=0))
    return active_cubes


def input_to_4d_points(data: List[str]) -> Set[Coord4D]:
    active_cubes = set()
    for i, line in enumerate(data):
        for j, char in enumerate(line):
            if char == "#":
                active_cubes.add(Coord4D(x=j, y=i, z=0, w=0))
    return active_cubes


def get_possible_changes_3d(active_cubes: Set[Coord3D]) -> Set[Coord3D]:
    possible_changes = active_cubes.copy()
    for point in active_cubes:
        possible_changes.update({point + neighbor for neighbor in NEIGHBORS_3D})
    return possible_changes


def get_possible_changes_4d(active_cubes: Set[Coord4D]) -> Set[Coord4D]:
    possible_changes = active_cubes.copy()
    for point in active_cubes:
        possible_changes.update({point + neighbor for neighbor in NEIGHBORS_4D})
    return possible_changes


def check_neighbors_3d(active_cubes: Set[Coord3D], point: Coord3D) -> int:
    total = 0
    for adjacent in {point + neighbor for neighbor in NEIGHBORS_3D}:
        if adjacent in active_cubes:
            total += 1
    return total


def check_neighbors_4d(active_cubes: Set[Coord4D], point: Coord4D) -> int:
    total = 0
    for adjacent in {point + neighbor for neighbor in NEIGHBORS_4D}:
        if adjacent in active_cubes:
            total += 1
    return total


def run_cycle_3d(active_cubes: Set[Coord3D]):
    new_active_cubes = active_cubes.copy()
    possible_changes = get_possible_changes_3d(active_cubes)
    for point in possible_changes:
        num_neighbors = check_neighbors_3d(active_cubes, point)
        if point in active_cubes and num_neighbors not in (2, 3):
            new_active_cubes.remove(point)
        elif point not in active_cubes and num_neighbors == 3:
            new_active_cubes.add(point)
    return new_active_cubes


def run_cycle_4d(active_cubes: Set[Coord4D]):
    new_active_cubes = active_cubes.copy()
    possible_changes = get_possible_changes_4d(active_cubes)
    for point in possible_changes:
        num_neighbors = check_neighbors_4d(active_cubes, point)
        if point in active_cubes and num_neighbors not in (2, 3):
            new_active_cubes.remove(point)
        elif point not in active_cubes and num_neighbors == 3:
            new_active_cubes.add(point)
    return new_active_cubes


TEST_INPUT = """.#.
..#
###""".split("\n")
INPUT = read_data().split("\n")

points_3d = input_to_3d_points(INPUT)
for _ in range(6):
    points_3d = run_cycle_3d(points_3d)

print(f"Total active 3D points: {len(points_3d)}")

points_4d = input_to_4d_points(INPUT)
for _ in range(6):
    points_4d = run_cycle_4d(points_4d)

print(f"Total active 4D points: {len(points_4d)}")


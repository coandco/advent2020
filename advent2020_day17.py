from utils import read_data
from typing import NamedTuple, List, Set, Union


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


def get_possible_changes(active_cubes: Union[Set[Coord3D], Set[Coord4D]],
                         neighbor_offsets: Union[List[Coord3D], List[Coord4D]]) -> Union[Set[Coord3D], Set[Coord4D]]:
    possible_changes = active_cubes.copy()
    for point in active_cubes:
        possible_changes.update({point + neighbor for neighbor in neighbor_offsets})
    return possible_changes


def check_neighbors(active_cubes: Union[Set[Coord3D], Set[Coord4D]], point: Union[Coord3D, Coord4D],
                       neighbor_offsets: Union[List[Coord3D], List[Coord4D]]) -> int:
    total = 0
    for adjacent in {point + neighbor for neighbor in neighbor_offsets}:
        if adjacent in active_cubes:
            total += 1
    return total


def run_cycle(active_cubes: Union[Set[Coord3D], Set[Coord4D]],
              neighbor_offsets: Union[List[Coord3D], List[Coord4D]]) -> Union[Set[Coord3D], Set[Coord4D]]:
    new_active_cubes = active_cubes.copy()
    possible_changes = get_possible_changes(active_cubes, neighbor_offsets)
    for point in possible_changes:
        num_neighbors = check_neighbors(active_cubes, point, neighbor_offsets)
        if point in active_cubes and num_neighbors not in (2, 3):
            new_active_cubes.remove(point)
        elif point not in active_cubes and num_neighbors == 3:
            new_active_cubes.add(point)
    return new_active_cubes


def main():
    cubes = read_data().splitlines()
    
    points_3d = input_to_3d_points(cubes)
    for _ in range(6):
        points_3d = run_cycle(points_3d, NEIGHBORS_3D)
    print(f"Part one: {len(points_3d)}")
    
    points_4d = input_to_4d_points(cubes)
    for _ in range(6):
        points_4d = run_cycle(points_4d, NEIGHBORS_4D)
    
    print(f"Part two: {len(points_4d)}")
    

if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")



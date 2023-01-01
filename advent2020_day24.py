from utils import read_data
from typing import NamedTuple, Dict, Set, List, DefaultDict
from collections import defaultdict


class Coord(NamedTuple):
    y: int
    x: int
    z: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(x=self.x + other.x, y=self.y + other.y, z=self.z+other.z)

    def __repr__(self) -> str:
        return f"Coord(x={self.x}, y={self.y}, z={self.z})"


DIR_OFFSETS: Dict[str, Coord] = {
    'se': Coord(1, 0, -1),
    'sw': Coord(0, 1, -1),
    'w': Coord(-1, 1, 0),
    'nw': Coord(-1, 0, 1),
    'ne': Coord(0, -1, 1),
    'e': Coord(1, -1, 0)
}


def dirstring_to_coord(dirstring: str) -> Coord:
    i = 0
    curloc = Coord(0, 0, 0)
    while i < len(dirstring):
        if dirstring[i] in ("w", "e"):
            curloc += DIR_OFFSETS[dirstring[i]]
            i += 1
        elif dirstring[i] in ("n", "s"):
            curloc += DIR_OFFSETS[dirstring[i:i+2]]
            i += 2
    return curloc


def make_field(data: List[str]) -> Set[Coord]:
    black_tiles: Set[Coord] = set()
    for line in data:
        line_coord = dirstring_to_coord(line)
        if line_coord in black_tiles:
            black_tiles.remove(line_coord)
        else:
            black_tiles.add(line_coord)
    return black_tiles


def get_neighbors(field: Set[Coord]) -> DefaultDict[Coord, int]:
    neighbors = defaultdict(int)
    for coord in field:
        for offset in DIR_OFFSETS.values():
            neighbors[coord+offset] += 1
    return neighbors


def run_iteration(field: Set[Coord]) -> Set[Coord]:
    new_field = field.copy()
    neighbors = get_neighbors(field)
    # Neighbors only contains neighbors of existing locations, not the locations themselves, so we add it to field
    for coord in field | neighbors.keys():
        if coord in field and (neighbors[coord] == 0 or neighbors[coord] > 2):
            new_field.remove(coord)
        elif coord not in field and neighbors[coord] == 2:
            new_field.add(coord)
    return new_field


def main():
    starting_field = make_field(read_data().splitlines())
    print(f"Part one: {len(starting_field)}")
    current_field = starting_field
    for i in range(100):
        current_field = run_iteration(current_field)
    print(f"Part two: {len(current_field)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

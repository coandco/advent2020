from utils import read_data
from typing import NamedTuple, Set, Tuple, List, Dict
from time import time


class Coord(NamedTuple):
    y: int
    x: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(y=self.y + other.y, x=self.x + other.x)


NEIGHBORS = {Coord(x=-1, y=-1), Coord(x=0, y=-1), Coord(x=1, y=-1),
             Coord(x=-1, y=0),                    Coord(x=1, y=0),
             Coord(x=-1, y=1),  Coord(x=0, y=1),  Coord(x=1, y=1)}


def in_bounds(shape: Tuple[int, int], coord: Coord) -> bool:
    return (0 <= coord.y < shape[0]) and (0 <= coord.x < shape[1])


class DictGrid:
    height: int
    width: int
    grid: Dict[Coord, bool]
    neighbors: Dict[Coord, Set[Coord]]

    def __init__(self, data: List[str], simple_neighbors: bool = True):
        self.height = len(data)
        self.width = len(data[0])
        self.grid = {}
        self.neighbors = {}
        self.simple_neighbors = simple_neighbors
        self.crowd_tolerance = 4 if simple_neighbors else 5
        for i, line in enumerate(data):
            for j, char in enumerate(line):
                if char == "#":
                    self.grid[Coord(y=i, x=j)] = True
                elif char == "L":
                    self.grid[Coord(y=i, x=j)] = False
                # Ignore floor and don't even have it in the dict
        if self.simple_neighbors:
            self._generate_part_one_neighbors()
        else:
            self._generate_part_two_neighbors()

    def _generate_part_one_neighbors(self):
        for coord in self.grid.keys():
            neighbor_set = set()
            for offset in NEIGHBORS:
                if coord + offset in self.grid:
                    neighbor_set.add(coord + offset)
            self.neighbors[coord] = neighbor_set

    def _generate_part_two_neighbors(self):
        for coord in self.grid.keys():
            neighbor_set = set()
            for offset in NEIGHBORS:
                current_coord = coord
                while in_bounds((self.height, self.width), current_coord := current_coord + offset):
                    if current_coord in self.grid:
                        neighbor_set.add(current_coord)
                        break
            self.neighbors[coord] = neighbor_set

    def _new_value(self, coord):
        test_count = 0
        if coord.x == 0 and coord.y == 1:
            test_count += 1
        num_neighbors = sum(self.grid[x] for x in self.neighbors[coord])
        if num_neighbors == 0:
            return True
        elif num_neighbors >= self.crowd_tolerance:
            return False
        else:
            return self.grid[coord]

    def convolute(self) -> bool:
        new_grid = {coord: self._new_value(coord) for coord in self.grid}
        any_changes = (self.grid != new_grid)
        self.grid = new_grid
        return any_changes

    def count_occupied(self):
        return len([x for x in self.grid if self.grid[x]])

    def __repr__(self):
        retval = ""
        for i in range(self.height):
            for j in range(self.width):
                value = self.grid.get(Coord(y=i, x=j), None)
                if value is None:
                    retval += "."
                elif value is True:
                    retval += "#"
                elif value is False:
                    retval += "L"
            retval += "\n"
        return retval


def part_one(data):
    start = time()
    grid = DictGrid(data)
    while grid.convolute():
        pass

    part_one_time = time() - start
    return grid.count_occupied(), part_one_time


def part_two(data):
    start = time()
    grid = DictGrid(data, simple_neighbors=False)
    while grid.convolute():
        pass

    part_two_time = time() - start
    return grid.count_occupied(), part_two_time


if __name__ == '__main__':
    INPUT = read_data().split("\n")
    part_one_result, part_one_time = part_one(INPUT)
    print(f"Part one resulted in {part_one_result} occupied seats, taking {part_one_time} seconds")

    part_two_result, part_two_time = part_two(INPUT)
    print(f"Part two resulted in {part_two_result} occupied seats, taking {part_two_time} seconds")
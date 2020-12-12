from utils import read_data
from typing import NamedTuple, List
from math import prod


class Coord(NamedTuple):
    y: int
    x: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(y=self.y + other.y, x=self.x + other.x)


def has_tree(treemap: List[str], loc: Coord) -> bool:
    if loc.y < 0 or loc.y >= len(treemap):
        return None
    if treemap[loc.y][loc.x % len(treemap[0])] == "#":
        return True
    else:
        return False


def check_slope(treemap: List[str], slope: Coord) -> int:
    num_trees = 0
    curpos = Coord(x=0, y=0)
    while (current_tree := has_tree(treemap, curpos)) is not None:
        if current_tree:
            num_trees += 1
        curpos += slope
    return num_trees


INPUT = read_data().split("\n")

SLOPES = [
    Coord(x=1, y=1),
    Coord(x=3, y=1),
    Coord(x=5, y=1),
    Coord(x=7, y=1),
    Coord(x=1, y=2)
]

if __name__ == '__main__':
    num_trees = check_slope(INPUT, Coord(x=3, y=1))
    print(f"Part one: {num_trees}")

    slope_trees = [check_slope(INPUT, x) for x in SLOPES]
    print(f"Part two: {prod(slope_trees)}")


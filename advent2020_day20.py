from utils import read_data
from dataclasses import dataclass
from typing import Tuple, FrozenSet, Dict
from math import prod
import numpy as np


DIRECTIONS = {'N': 0, 'W': 1, 'S': 2, 'E': 3}
ROTATED_DIRECTIONS = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}



@dataclass
class Tile:
    tile_id: int
    tile_data: Tuple[Tuple[bool, ...], ...]
    sides: Tuple[Tuple[bool], ...]
    reversed_sides: Tuple[Tuple[bool], ...]

    def side_fits(self, side: Tuple[bool]):
        return side in self.sides or side in self.reversed_sides

    def find_rotation(self, other_tile: 'Tile'):
        for i, side in enumerate(self.sides):
            for j, other_side in enumerate(other_tile.sides):
                if side == other_side:
                    flipped = False
                    return i, j, flipped
            for j, other_side in enumerate(other_tile.reversed_sides):
                if side == other_side:
                    flipped = True
                    return i, j, flipped

    @staticmethod
    def from_string(data: str) -> 'Tile':
        lines = data.split("\n")
        tile_id = int(lines[0].split("Tile ")[1][:-1])
        tile_data = []
        for line in lines[1:]:
            tile_data.append(tuple(char == "#" for char in line))
        # Sides:     0
        #            -
        #         1 | | 3
        #            -
        #            2
        sides = tuple([tuple(tile_data[0]),
                      tuple(x[0] for x in tile_data),
                      tuple(tile_data[-1]),
                      tuple(x[-1] for x in tile_data)
                      ])
        reversed_sides = tuple([tuple(reversed(x)) for x in sides])
        return Tile(tile_id=tile_id, tile_data=tuple(tile_data), sides=sides, reversed_sides=reversed_sides)

    def __repr__(self):
        output = [f"Tile {self.tile_id}:"]
        for line in self.tile_data:
            output.append("".join("#" if x else "." for x in line))
        return "\n".join(output)


def get_matching_tiles(tile_dict: Dict[int, Tile], tile: Tile):
    matching_tiles = set()
    for other_tile in tile_dict.values():
        if other_tile.tile_id == tile.tile_id:
            # This is yourself, skip it
            continue
        for side in tile.sides:
            if other_tile.side_fits(side):
                matching_tiles.add(other_tile.tile_id)
    return matching_tiles


TEST_DATA = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""

test_tiles = {Tile.from_string(x).tile_id: Tile.from_string(x) for x in TEST_DATA.split("\n\n")}
matching_tiles = {x: get_matching_tiles(test_tiles, test_tiles[x]) for x in test_tiles.keys()}
#a = test_tiles[1951].find_rotation(test_tiles[2311])
print(prod(x for x in matching_tiles.keys() if len(matching_tiles[x]) == 2))




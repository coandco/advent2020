from utils import read_data
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, List, Set, NamedTuple
from math import prod
import numpy as np


DIRECTIONS = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
ROTATED_DIRECTIONS = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
ROTATED_DIRECTION_INTS = {DIRECTIONS[k]: DIRECTIONS[v] for k, v in ROTATED_DIRECTIONS.items()}


class Coord(NamedTuple):
    y: int
    x: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(x=self.x + other.x, y=self.y + other.y)

    def __repr__(self) -> str:
        return f"Coord(x={self.x}, y={self.y})"


@dataclass(frozen=True)
class FrozenTile:
    tile_id: int
    tile_data: Tuple[Tuple[bool, ...], ...]
    sides: Tuple[Tuple[bool], ...]
    reversed_sides: Tuple[Tuple[bool], ...]

    def side_fits(self, side: Tuple[bool]):
        return side in self.sides or side in self.reversed_sides

    def find_rotation(self, other_tile: 'FrozenTile'):
        for i, side in enumerate(self.sides):
            for j, other_side in enumerate(other_tile.sides):
                if side == other_side:
                    flipped = False
                    return i, j, flipped
            for j, other_side in enumerate(other_tile.reversed_sides):
                if side == other_side:
                    flipped = True
                    return i, j, flipped

    def occupied_sides(self, other_tiles: Set['FrozenTile']) -> Set[int]:
        occupied = set()
        for i, side in enumerate(self.sides):
            for other_tile in other_tiles:
                if side in other_tile.sides or side in other_tile.reversed_sides:
                    occupied.add(i)
        return occupied

    @staticmethod
    def from_string(data: str) -> 'FrozenTile':
        lines = data.split("\n")
        tile_id = int(lines[0][5:-1])
        tile_data = []
        for line in lines[1:]:
            tile_data.append(tuple(char == "#" for char in line))
        # Sides:     0
        #            -
        #         3 | | 1
        #            -
        #            2
        sides = tuple([tuple(tile_data[0]),
                      tuple(x[-1] for x in tile_data),
                      tuple(tile_data[-1]),
                      tuple(x[0] for x in tile_data)
                      ])
        reversed_sides = tuple([tuple(reversed(x)) for x in sides])
        return FrozenTile(tile_id=tile_id, tile_data=tuple(tile_data), sides=sides, reversed_sides=reversed_sides)

    def __repr__(self):
        output = [f"Tile {self.tile_id}:"]
        for line in self.tile_data:
            output.append("".join("#" if x else "." for x in line))
        return "\n".join(output)


@dataclass
class NPTile:
    tile_id: int
    tile_data: np.ndarray
    right_tile: Optional['NPTile'] = None
    down_tile: Optional['NPTile'] = None

    @staticmethod
    def from_string(data: str) -> 'NPTile':
        lines = data.split("\n")
        tile_id = int(lines[0][5:-1])
        tile_data = []
        for line in lines[1:]:
            tile_data.append([1 if char == "#" else 0 for char in line])
        tile_data_np = np.ndarray(tile_data, dtype=int)
        return NPTile(tile_id=tile_id, tile_data=tile_data_np)

    @staticmethod
    def from_frozen_tile(tile: FrozenTile) -> 'NPTile':
        return NPTile(tile_id=tile.tile_id, tile_data=np.array(tile.tile_data, dtype=int))

    @property
    def sides(self) -> Tuple[np.ndarray, ...]:
        return tuple([self.tile_data[0, :],
                      self.tile_data[:, -1],
                      self.tile_data[-1, :],
                      self.tile_data[:, 0]])

    @property
    def reversed_sides(self) -> Tuple[np.ndarray, ...]:
        return tuple([np.flip(x) for x in self.sides])

    @property
    def without_borders(self) -> np.ndarray:
        return self.tile_data[1:-1, 1:-1]

    def rotate(self, times: int = 1):
        self.tile_data = np.rot90(self.tile_data, times, axes=(1, 0))

    def flipud(self):
        self.tile_data = np.flipud(self.tile_data)

    def match(self, side_num: int, side: np.ndarray):
        for _ in range(4):
            self.rotate()
            if np.array_equal(self.sides[side_num], side):
                return True
        self.flipud()
        for _ in range(4):
            self.rotate()
            if np.array_equal(self.sides[side_num], side):
                return True
        return False

    def get_full_web(self, borders=True):
        full_web = None
        line_start = self

        while line_start is not None:
            line_buffer = None
            current_tile = line_start
            while current_tile is not None:
                if borders:
                    current_ndarray = current_tile.tile_data
                else:
                    current_ndarray = current_tile.without_borders

                if line_buffer is None:
                    line_buffer = current_ndarray
                else:
                    line_buffer = np.concatenate((line_buffer, current_ndarray), axis=1)

                current_tile = current_tile.right_tile
            if full_web is None:
                full_web = line_buffer
            else:
                full_web = np.concatenate((full_web, line_buffer), axis=0)
            line_start = line_start.down_tile
        return full_web

    def repr_with_spacing(self, borders=True) -> List[str]:
        buffer = []
        line_start = self
        line_height = self.tile_data.shape[0] if borders else self.without_borders.shape[0]
        # loop over lines
        while line_start is not None:
            line_buffer = [""] * line_height
            current_tile = line_start
            # Loop over tiles in the line
            while current_tile is not None:
                for i in range(line_height):
                    slice = current_tile.tile_data[i, :] if borders else current_tile.without_borders[i, :]
                    line_buffer[i] += "".join(["#" if x else "." for x in slice])
                    line_buffer[i] += " "
                current_tile = current_tile.right_tile
            # Once we finish a line, append it to the buffer, followed by a blank line
            buffer.extend(line_buffer)
            buffer.append("")
            line_start = line_start.down_tile
        return buffer

    def repr_without_spacing(self, borders=True) -> List[str]:
        buffer = []
        full_web = self.get_full_web(borders=borders)
        for row in full_web:
            buffer.append("".join("#" if x else "." for x in row))
        return buffer


def get_matching_tiles(tile_dict: Dict[int, FrozenTile], tile: FrozenTile) -> Set[FrozenTile]:
    matching_tiles = set()
    for other_tile in tile_dict.values():
        if other_tile.tile_id == tile.tile_id:
            # This is yourself, skip it
            continue
        for side in tile.sides:
            if other_tile.side_fits(side):
                matching_tiles.add(other_tile)
    return matching_tiles


def get_corner_rotation(dir_set: Set[int]) -> int:
    for i in range(4):
        # We want the first piece to be the top-left one
        if dir_set == {DIRECTIONS['E'], DIRECTIONS['S']}:
            return i
        else:
            new_dirs = set()
            for dir in dir_set:
                new_dirs.add(ROTATED_DIRECTION_INTS[dir])
            dir_set = new_dirs


def build_nptile_web(tile_set: Dict[int, FrozenTile], matching_tiles: Dict[int, Set[FrozenTile]], first_piece: Optional[NPTile] = None):
    if not first_piece:
        corners = [tile_set[x] for x in matching_tiles.keys() if len(matching_tiles[x]) == 2]
        top_left = corners[0]
        occupied_sides = top_left.occupied_sides(matching_tiles[top_left.tile_id])
        first_piece = NPTile.from_frozen_tile(top_left)
        first_piece_rotation = get_corner_rotation(occupied_sides)
        first_piece.rotate(first_piece_rotation)

    current_line_start = first_piece
    # For each line
    while True:
        # Exit the loop if we've tried to go down and have reached the end
        if current_line_start is None:
            break
        current_piece = current_line_start
        # For each element in the line
        while True:
            for possible_next_piece in [NPTile.from_frozen_tile(x) for x in matching_tiles[current_piece.tile_id]]:
                if possible_next_piece.match(DIRECTIONS['W'], current_piece.sides[DIRECTIONS['E']]):
                    current_piece.right_tile = possible_next_piece
                elif possible_next_piece.match(DIRECTIONS['N'], current_piece.sides[DIRECTIONS['S']]):
                    current_piece.down_tile = possible_next_piece
            if current_piece.right_tile:
                current_piece = current_piece.right_tile
                continue
            else:
                # We've reached the end of the line, go to the next line if possible
                current_line_start = current_line_start.down_tile
                break
    return first_piece


SEA_MONSTER = [
    "                  #  ",
    "#    ##    ##    ### ",
    " #  #  #  #  #  #    "
]


def get_sea_monster_coords(monster_shape: List[str]) -> Set[Coord]:
    sea_monster_coords = set()
    for i, line in enumerate(monster_shape):
        for j, char in enumerate(line):
            if char == "#":
                sea_monster_coords.add(Coord(y=i, x=j))
    return sea_monster_coords


SEA_MONSTER_COORDS = get_sea_monster_coords(SEA_MONSTER)


def find_sea_monsters(grid: np.ndarray) -> int:
    sea_monster_height = len(SEA_MONSTER)
    sea_monster_width = len(SEA_MONSTER[0])
    num_monsters = 0
    for i in range(0, grid.shape[0] - sea_monster_height):
        for j in range(0, grid.shape[1] - sea_monster_width):
            slice = grid[i:i+sea_monster_height, j:j+sea_monster_width]
            if all(slice[coord] == 1 for coord in SEA_MONSTER_COORDS):
                num_monsters += 1
    return num_monsters


def find_monsters_any_orientation(grid: np.ndarray) -> int:
    for _ in range(4):
        grid = np.rot90(grid, 1, axes=(1, 0))
        num_monsters = find_sea_monsters(grid)
        if num_monsters > 0:
            return num_monsters
    grid = np.flipud(grid)
    for _ in range(4):
        grid = np.rot90(grid, 1, axes=(1, 0))
        num_monsters = find_sea_monsters(grid)
        if num_monsters > 0:
            return num_monsters


def part_one(data: str) -> Tuple[Dict[int, FrozenTile], Dict[int, Set[FrozenTile]], int]:
    tile_dict = {FrozenTile.from_string(x).tile_id: FrozenTile.from_string(x) for x in data.split("\n\n")}
    matching_tiles = {x: get_matching_tiles(tile_dict, tile_dict[x]) for x in tile_dict.keys()}
    return tile_dict, matching_tiles, prod(x for x in matching_tiles.keys() if len(matching_tiles[x]) == 2)


def part_two(all_tiles: Dict[int, FrozenTile], neighbors: Dict[int, Set[FrozenTile]]) -> int:
    top_left = build_nptile_web(all_tiles, neighbors)
    full_web = top_left.get_full_web(borders=False)
    num_monsters = find_monsters_any_orientation(full_web)
    return np.count_nonzero(full_web) - len(SEA_MONSTER_COORDS)*num_monsters


if __name__ == '__main__':
    frozen_tiles, matching_tile_dict, part_one_answer = part_one(read_data())
    print(f'Part one: {part_one_answer}')
    print(f"Part two: {part_two(frozen_tiles, matching_tile_dict)}")





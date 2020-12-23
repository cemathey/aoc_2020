import sys
from pprint import pprint
from typing import NamedTuple, Tuple, Dict, List, Generator
from collections import deque
from functools import reduce
from itertools import combinations, permutations, cycle
from copy import deepcopy


class Tile(NamedTuple):
    tile_id: int
    size: int
    pixels: Tuple[Tuple[str, ...], ...]


class Image(NamedTuple):
    size: int
    pixels: Tuple[Tuple[str, ...], ...]


def build_tile(tile_lines: str):
    """Build a new tile from the given string."""
    tile_lines = tile_lines.split("\n")
    tile_id = int(tile_lines[0][4:-1])
    size = len(tile_lines[1])
    pixels = tuple(tuple(line) for line in tile_lines[1:])

    tile = Tile(tile_id, size, pixels)
    return tile


def build_tiles(file_name):
    """Return a dictionary of tiles contained in the file."""
    raw_tiles = [raw_tile for raw_tile in open(filename).read().split("\n\n")]

    tiles = [build_tile(raw_tile) for raw_tile in raw_tiles]
    tiles = {tile.tile_id: tile for tile in tiles}

    return tiles


def vertical_flip(tile):
    """Perform a vertical flip (bottom to top) of the given tile and return the new, flipped tile."""
    new_pixels = tuple(row for row in reversed(tile.pixels))

    return Tile(tile.tile_id, tile.size, new_pixels)


def rotate_tile_90(tile):
    """Perform a 90* clockwise rotation of the given tile and return the new, rotated tile."""

    new_pixels = [[None] * tile.size for _ in range(tile.size)]

    points = deque()
    col = 0
    for _ in range(tile.size):
        for row in range(tile.size - 1, -1, -1):
            points.append((row, col))
        col += 1

    for i in range(tile.size):
        for j in range(tile.size):
            rot_i, rot_j = points.popleft()
            new_pixels[i][j] = tile.pixels[rot_i][rot_j]

    new_pixels = tuple(tuple(row) for row in new_pixels)

    return Tile(tile.tile_id, tile.size, new_pixels)


def rotate_tile(tile, degrees=90):
    """Rotate the given tile the indicated degrees and return the new, rotated title"""
    assert degrees in (90, 180, 270, 360)

    times = degrees // 90

    if degrees == 360:
        return tile

    for _ in range(times):
        tile = rotate_tile_90(tile)

    return tile


def top_edge(tile: Tile) -> Tuple[str, ...]:
    """Return the top edge of the tile."""
    return tile.pixels[0]


def bottom_edge(tile: Tile) -> Tuple[str, ...]:
    """Return the bottom edge of the tile."""
    return tile.pixels[-1]


def left_edge(tile: Tile) -> Tuple[str, ...]:
    """Return the left edge of the tile."""
    return tuple(row[0] for row in tile.pixels)


def right_edge(tile: Tile) -> Tuple[str, ...]:
    """Return the right edge of the tile."""
    return tuple(row[-1] for row in tile.pixels)


def all_tile_orientations(tile: Tile) -> Generator:
    """Yield all orientations of the given tile."""
    # A horizontal and vertical flip == 180* rotation
    yield tile
    yield vertical_flip(tile)

    for degree in (90, 180, 270):
        rotated_tile = rotate_tile(tile, degree)
        yield rotated_tile

        v_flipped_tile = vertical_flip(rotated_tile)
        yield v_flipped_tile


def rotate_flip_all_tiles(tiles_lookup: Dict[int, Tile]) -> Generator:
    """Yield a tile in each orientation."""
    for tile in tiles_lookup.values():
        for oriented_tile in all_tile_orientations(tile):
            yield oriented_tile


def top_matching_tile(tiles_lookup, top_tile):
    """From the given tile, find a tile whose top edge matches the bottom edge of top_tile or None."""
    for potential_match in rotate_flip_all_tiles(tiles_lookup):
        if bottom_edge(top_tile) == top_edge(potential_match):
            return potential_match

    return None


def left_matching_tile(tiles_lookup, left_tile):
    """From the given tile, find a tile whose left edge matches the right edge of left_tile or None."""
    for potential_match in rotate_flip_all_tiles(tiles_lookup):
        if right_edge(left_tile) == left_edge(potential_match):
            return potential_match

    return None


def top_left_corner_possibilities(tiles_lookup, tile):
    """From the given corner tile, check all possible orientations for a valid grid fill starting from that orientation."""
    oriented_tiles = list(all_tile_orientations(tile))
    for top_left in all_tile_orientations(tile):
        grid = attempt_grid_fill(tiles_lookup, top_left)
        if grid:
            return grid

    return None


def attempt_grid_fill(tiles_lookup, starting_tile):
    """From the given tiles in tiles_lookup and a starting tile, attempt to fill the grid from left to right, top to bottom."""
    grid_size = int(len(tiles_lookup) ** 0.5)
    grid = [[None] * grid_size for _ in range(grid_size)]

    # Make a copy of our available tiles so we can mutate it and remove the starting_tile from consideration
    available_tiles = deepcopy(tiles_lookup)
    del available_tiles[starting_tile.tile_id]

    grid[0][0] = starting_tile
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            potential_match = None

            # Top left corner is prefilled, skip it
            if (i, j) == (0, 0):
                continue

            # The very first entry in every row needs to match the tile above it
            if j == 0:
                top_tile = grid[i - 1][j]
                potential_match = top_matching_tile(available_tiles, top_tile)
            # All other entries must match the right edge of the tile to the left
            else:
                left_tile = grid[i][j - 1]
                potential_match = left_matching_tile(available_tiles, left_tile)

            if potential_match:
                grid[i][j] = potential_match
                del available_tiles[potential_match.tile_id]
            else:
                # Unable to find a matching tile for the given grid cell
                return None

    return grid


def remove_tile_borders(tile: Tile) -> Tile:
    """Return a new tile with the borders of the original tile removed."""
    new_pixels = []

    # From the 2nd row to the 2nd to last row
    # From the 2nd col to the 2nd to last col

    for row in tile.pixels[1:-1]:
        new_pixels.append(row[1:-1])

    tile_size = len(new_pixels)
    return Tile(tile.tile_id, tile_size, tuple(tuple(row) for row in new_pixels))


def remove_borders(grid: Tuple[Tile, ...]):
    borders_removed = []
    for row in grid:
        new_row = []
        for tile in row:
            new_row.append(remove_tile_borders(tile))
        borders_removed.append(new_row)

    return borders_removed


def grab_corner_tiles(grid: Tuple[Tile, ...]):
    return (grid[0][0], grid[0][-1], grid[-1][-1], grid[-1][0])


def stitch_tiles(grid: Tuple[Tile, ...]) -> Image:
    """Take the given grid of tiles, remove the border of each tile, and assemble them into one large tile."""
    trimmed_grid = remove_borders(grid)
    tile_size = trimmed_grid[0][0].size
    image_size = len(trimmed_grid[0][0].pixels) * len(trimmed_grid[0])
    pixels = [[None] * image_size for _ in range(image_size)]

    i_offsets = cycle(range(8))
    j_offsets = cycle(range(1, 24))

    # Row 1
    # tile 1:
    # i=0 to i=7
    # j=0 to j=7

    # tile 1:
    # i=0 to i=7
    # j=8 to j=15

    # tile 3:
    # i=0 to i=7
    # j=16 to j=23

    # Row 2
    # tile 4:
    # i=8 to i=15
    # j=0 to j=7

    # tile 5:
    # i=8 to i=15
    # j=8 to j=15

    # tile 6:
    # i=8 to i=15
    # j=16 to j=23

    i_offsets = [range(0, 8), range(8, 16), range(16, 24)]
    j_offsets = [range(0, 8), range(8, 16), range(16, 24)]

    for row in trimmed_grid:
        for tile in row:
            for pixel_i, pixel_row in enumerate(tile.pixels):
                for pixel_j, pixel in enumerate(pixel_row):
                    pixels[i][j] = pixel

    return Image(image_size, tuple(tuple(row) for row in pixels))


if __name__ == "__main__":
    filename = sys.argv[1]
    tiles_lookup = build_tiles(filename)

    grid = None
    for tile in tiles_lookup.values():
        grid = top_left_corner_possibilities(tiles_lookup, tile)
        if grid:
            break

    assert grid
    corner_tiles = grab_corner_tiles(grid)
    answer = reduce(lambda total, tile: total * tile.tile_id, corner_tiles, 1)
    assert answer == 20899048083289
    print(f"Part 1: Corner Tile Product {answer}")

    # stitch_tiles(grids[0])

import sys
from pprint import pprint
from typing import NamedTuple, Tuple, Dict, List
from collections import deque
from functools import reduce
from itertools import combinations, permutations


class Tile(NamedTuple):
    tile_id: int
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


def horizontal_flip(tile):
    """Perform a horizontal flip (right to left) of the given tile and return the new, flipped tile."""
    new_pixels = tuple(tuple(reversed(row)) for row in tile.pixels)

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

    if times == 4:
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


def border_matches(tile_one: Tile, tile_two: Tile) -> int:
    """Compare each edge of tile_one against each edge of tile_two and return the number of matches."""
    matching_functions = (top_edge, bottom_edge, left_edge, right_edge)
    count: int = 0

    # Compare all like edges
    for matcher in matching_functions:
        if matcher(tile_one) == matcher(tile_two):
            count += 1

    # Compare opposite edges
    if left_edge(tile_one) == right_edge(tile_two):
        count += 1

    if right_edge(tile_one) == left_edge(tile_two):
        count += 1

    if top_edge(tile_one) == bottom_edge(tile_two):
        count += 1

    if bottom_edge(tile_one) == top_edge(tile_two):
        count += 1

    return count


def count_border_matches(tiles_lookup: Dict[int, Tile], tile: Tile):
    """Compare the given tile against all other tiles, rotating and flipping them."""
    count = 0
    for test_tile_id in tiles_lookup.keys():
        # Never check yourself
        if test_tile_id == tile.tile_id:
            continue
        test_tile = tiles_lookup[test_tile_id]

        # Rotate AND flip through all the orientations including the original (360)
        for degree in (90, 180, 270, 360):
            rotated_tile = rotate_tile(test_tile, degree)
            h_flipped_tile = horizontal_flip(rotated_tile)
            count += border_matches(tile, h_flipped_tile)

    return count


def border_matches_counts(tiles_lookup: Dict[int, Tile]) -> List[int]:
    """For each tile, count the number of borders that match other tiles."""
    matching_borders_counts: List[int] = []

    # For each tile, iterate through every other tile in each of its orientations and count the matching borders
    for tile_id in tiles_lookup.keys():
        tile = tiles_lookup[tile_id]
        count = count_border_matches(tiles_lookup, tile)
        matching_borders_counts.append(count)

    return matching_borders_counts


def find_corner_tiles(tiles_lookup):
    matching_counts = border_matches_counts(tiles_lookup)

    corner_tiles = [
        tile_id
        for tile_id, matches in zip(tiles_lookup.keys(), matching_counts)
        if matches == 2
    ]

    return corner_tiles


if __name__ == "__main__":
    filename = sys.argv[1]
    tiles_lookup = build_tiles(filename)
    grid_size = int(len(tiles_lookup) ** 0.5)

    corner_tiles = find_corner_tiles(tiles_lookup)
    answer = reduce(lambda total, tile_id: total * tile_id, corner_tiles, 1)
    print(f"{corner_tiles=}")
    print(f"Part 1: Corner Tile Product {answer}")

    # The corner tiles can be in any of 24 orientations
    for combo in permutations(corner_tiles, 4):
        grid = [[None] * grid_size for _ in range(grid_size)]
        available_tiles = tiles_lookup.copy()

        # Assign these to the top left, top right, bottom right, bottom left slots accordingly
        top_left, top_right, bottom_right, bottom_left = combo

        grid[0][0] = top_left
        grid[0][-1] = top_right
        grid[-1][0] = bottom_left
        grid[-1][-1] = bottom_right

        # Remove our corner tiles from consideration
        for tile_id in combo:
            del available_tiles[tile_id]

        # Starting with our top left corner, there should be one and only one remaining tile that matches on exactly 2 edges
        # If there isn't, this is an invalid corner tile combination

        # tile = tiles_lookup[top_left]
        # matching_counts = []
        # for tile_ids in available_tiles.keys():
        #     count = border_matches()

        # print(f"corners={combo} {matching_counts=}")

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


def vertical_flip_pixels(pixels):
    return tuple(row for row in reversed(pixels))


def vertical_flip_tile(tile):
    """Perform a vertical flip (bottom to top) of the given tile and return the new, flipped tile."""
    return Tile(tile.tile_id, tile.size, vertical_flip_pixels(tile.pixels))


def vertical_flip_image(image):
    """Perform a vertical flip (bottom to top) of the given image and return the new, flipped image."""
    return Image(image.size, vertical_flip_pixels(image.pixels))


def rotate_pixels_90(pixels):
    size = len(pixels)
    new_pixels = [[None] * size for _ in range(size)]

    points = deque()
    col = 0
    for _ in range(size):
        for row in range(size - 1, -1, -1):
            points.append((row, col))
        col += 1

    for i in range(size):
        for j in range(size):
            rot_i, rot_j = points.popleft()
            new_pixels[i][j] = pixels[rot_i][rot_j]

    return tuple(tuple(row) for row in new_pixels)


def rotate_image_90(image):
    """Perform a 90* clockwise rotation of the given image and return the new, rotated image."""
    return Image(image.size, rotate_pixels_90(image.pixels))


def rotate_tile_90(tile):
    """Perform a 90* clockwise rotation of the given tile and return the new, rotated tile."""
    return Tile(tile.tile_id, tile.size, rotate_pixels_90(tile.pixels))


def rotate(item, degrees=90):
    """Rotate the given image or tile the indicated degrees and return the new, rotated item."""
    assert degrees in (90, 180, 270, 360)

    times = degrees // 90

    if degrees == 360:
        return item

    for _ in range(times):
        if type(item) == Tile:
            item = rotate_tile_90(item)
        elif type(item) == Image:
            item = rotate_image_90(item)

    return item


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


def all_image_orientations(image: Image) -> Generator:
    """Yield all orientations of the given image."""
    yield image
    yield vertical_flip_image(image)

    for degree in (90, 180, 270):
        rotated_image = rotate(image, degree)
        yield rotated_image

        v_flipped_image = vertical_flip_image(rotated_image)
        yield v_flipped_image


def all_tile_orientations(tile: Tile) -> Generator:
    """Yield all orientations of the given tile."""
    # A horizontal and vertical flip == 180* rotation
    yield tile
    yield vertical_flip_tile(tile)

    for degree in (90, 180, 270):
        rotated_tile = rotate(tile, degree)
        yield rotated_tile

        v_flipped_tile = vertical_flip_tile(rotated_tile)
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
    """Remove the borders from each tile in the grid and return a new grid."""
    trimmed_grid = []
    for row in grid:
        new_row = []
        for tile in row:
            new_row.append(remove_tile_borders(tile))
        trimmed_grid.append(new_row)

    return trimmed_grid


def grab_corner_tiles(grid: Tuple[Tile, ...]):
    """Return the corner tiles clockwise from the top left."""
    return (grid[0][0], grid[0][-1], grid[-1][-1], grid[-1][0])


def stitch_tiles(grid: Tuple[Tile, ...]) -> Image:
    """Take the given grid of tiles, remove the border of each tile, and assemble them into one image."""
    trimmed_grid = remove_borders(grid)
    image_size = len(trimmed_grid[0][0].pixels) * len(trimmed_grid[0])

    image_pixels = []
    for grid_row in trimmed_grid:
        first_tile = grid_row[0]
        # Stitch together a complete row from each tile in that row
        for i, pixel_row in enumerate(first_tile.pixels):
            image_row = []
            image_row.extend(pixel_row)
            for remaining_tile in grid_row[1:]:
                image_row.extend(remaining_tile.pixels[i])
            image_pixels.append(image_row)

    return Image(image_size, tuple(tuple(row) for row in image_pixels))


def fill_grid(tiles_lookup):
    """Return a solved grid if possible from the given tiles."""
    for tile in tiles_lookup.values():
        grid = top_left_corner_possibilities(tiles_lookup, tile)
        if grid:
            yield grid


def count_monsters(image: Image, monster_pixel="#") -> int:
    monster_point_offsets = [
        (0, 18),
        (1, 0),
        (1, 5),
        (1, 6),
        (1, 11),
        (1, 12),
        (1, 17),
        (1, 18),
        (1, 19),
        (2, 1),
        (2, 4),
        (2, 7),
        (2, 10),
        (2, 13),
        (2, 16),
    ]

    monster_length = 3
    monster_width = 21

    # Iterate through our image and look for monsters
    monster_count = 0
    for i, row in enumerate(image.pixels[:-monster_length]):
        for j, pixel in enumerate(row[:-monster_width]):
            offset_pixels = [(x + i, y + j) for x, y in monster_point_offsets]
            matches = [
                image.pixels[i + x][j + y] == monster_pixel
                for x, y in monster_point_offsets
            ]
            if all(
                image.pixels[x + i][y + j] == monster_pixel
                for x, y in monster_point_offsets
            ):
                monster_count += 1

    return monster_count


def find_correct_image_orientation(grids):
    for grid in grids:
        image = stitch_tiles(grid)
        for test_image in all_image_orientations(image):
            count = count_monsters(test_image)
            if count > 0:
                return test_image, count

    return None, None


if __name__ == "__main__":
    filename = sys.argv[1]
    tiles_lookup = build_tiles(filename)

    grids = list(fill_grid(tiles_lookup))
    assert len(grids) == 4

    corner_tiles = grab_corner_tiles(grids[0])
    assert len(corner_tiles) == 4

    answer = reduce(lambda total, tile: total * tile.tile_id, corner_tiles, 1)
    # assert answer == 20899048083289
    print(f"Part 1: Corner Tile Product {answer}")

    correct_image, monster_count = find_correct_image_orientation(grids)

    pound_count = 0
    for row in correct_image.pixels:
        for pixel in row:
            if pixel == "#":
                pound_count += 1

    answer = pound_count - monster_count * 15
    print(f"Part 2: answer={answer}")

    # for row in image.pixels:
    #     print("".join(row))

    # for row in image.pixels:
    #     for pixel in row:
    #         if pixel == "#":
    #             print(pixel, end="")
    #         else:
    #             print(" ", end="")
    #     print()

    # print()
    # print()

    # count = count_monsters(image)
    # print(f"{count=}")

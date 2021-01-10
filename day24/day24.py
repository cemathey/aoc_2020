from os import DirEntry
import sys
from collections import defaultdict, Counter
from pprint import pprint
from typing import Generator, Tuple


VALID_DIRECTIONS = ("e", "w", "ne", "nw", "se", "sw")


def parse_directions(lines):
    all_directions = []

    for line in lines:
        tile_directions = []

        half_direction = ""
        for char in line.strip():
            if half_direction:
                half_direction += char
                tile_directions.append(half_direction)
                half_direction = ""
            elif char in ("n", "s"):
                half_direction = char
            else:
                tile_directions.append(char)
        all_directions.append(tile_directions)

    return all_directions


def optimize_directions(directions):
    def remove_redundancy(one, two, new_direction):
        removed = 0
        if direction_count[one] and direction_count[two]:
            removed += 1
            if direction_count[one] >= direction_count[two]:
                delta = direction_count[two]
                direction_count[one] -= delta
                del direction_count[two]
            else:
                delta = direction_count[one]
                direction_count[two] -= delta
                del direction_count[one]

            if new_direction:
                direction_count[new_direction] += delta

        return removed

    # se, ne = e
    # sw, nw = w
    # e, w cancel
    # nw, se cancel
    # sw, ne cancel
    redundancies = (
        ("ne", "se", "e"),
        ("nw", "sw", "w"),
        ("ne", "w", "nw"),
        ("nw", "e", "ne"),
        ("se", "w", "sw"),
        ("sw", "e", "se"),
        ("e", "w", None),
        ("nw", "se", None),
        ("ne", "sw", None),
    )

    direction_count = Counter(directions)

    # Try to remove each type of redundancies until our directions stop shrinking
    removed = 1
    while removed != 0:
        removed = 0

        for one, two, new in redundancies:
            removed += remove_redundancy(one, two, new)

    # Rebuild a directions list
    new_directions = []
    for direction, count in direction_count.items():
        new_directions.extend([direction] * count)

    return new_directions


def get_destination_coords(path_to_tile):
    """Generate a coordinates for the tile at the end of the given path."""
    x: int = 0
    y: complex = 0 + 0j

    optimized_directions = optimize_directions(path_to_tile)
    for direction in optimized_directions:
        if direction == "ne":
            y += 1 + 1j
        elif direction == "nw":
            y += 1 - 1j
        elif direction == "se":
            y += -1 + 1j
        elif direction == "sw":
            y += -1 - 1j
        elif direction == "e":
            x += 1
        else:
            x -= 1

    return (x, y)


def get_neighbors(point: Tuple[int, int]) -> Generator:
    """Generate the coordinates for each tile adjacent to the given point."""
    x, y = point

    # (0, -1+1j)
    # (0, +1-1j)
    # (-1, -1+1j)
    # (-1, 0+0j)
    # (+1, +1-1j)
    # (+1, 0+0j)

    yield x, y + (-1 + 1j)
    yield x, y + (1 - 1j)
    yield x - 1, y + (-1 + 1j)
    yield x - 1, y + (0 + 0j)
    yield x + 1, y + (1 - 1j)
    yield x + 1, y + (0 + 0j)


def count_neighbors(floor, point):
    """Count the black tiles that neighbor the given point."""
    black_neighbors = 0

    for neighbor in get_neighbors(point):
        if floor.get(neighbor, False):
            black_neighbors += 1

    return black_neighbors


def set_initial_floor(directions):
    # False = white
    # True = black
    floor = dict()

    for tile_path in directions:
        x, y = get_destination_coords(tile_path)
        state = floor.get((x, y), False)
        floor[x, y] = not state

    return floor


if __name__ == "__main__":
    filename = sys.argv[1]
    contents = open(filename).readlines()
    directions = parse_directions(contents)

    floor = set_initial_floor(directions)

    tile_count = Counter(floor.values())
    print(f"Part 1 Black Tiles: {tile_count[True]} White Tiles: {tile_count[False]}")

    # point = (0, -2 - 2j)
    # for neighbor in get_neighbors(point):
    #     print(f"{neighbor=}")
    # black_neighbors = count_neighbors_complex(floor, point)
    # print(f"{point=} black:{black_neighbors}")

    for _ in range(1, 3):
        new_floor = floor.copy()
        for point, state in floor.items():
            black_neighbors = count_neighbors(floor, point)

            # Black tiles
            if floor[point]:
                if black_neighbors == 0 or black_neighbors > 2:
                    new_floor[point] = not floor[point]
            # White tiles
            else:
                if black_neighbors == 2:
                    new_floor[point] = not floor[point]

        floor = new_floor.copy()
        tile_count = Counter(floor.values())
        print(
            f"{_} days Black Tiles: {tile_count[True]} White Tiles: {tile_count[False]}"
        )

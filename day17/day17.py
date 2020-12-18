import sys
from typing import Sequence, Dict, Tuple, Union, List

ACTIVE = "#"
INACTIVE = "."
CYCLE_LIMIT = 6


def initialize_grid(lines: Sequence[str], dimensions: int = 3, z: int = 0, w: int = 0):
    """Generate the point and the initial state of that point from the given input lines."""
    assert dimensions in (3, 4)

    grid: Dict[Tuple[int, ...], str] = {}

    point: Tuple[int, ...]
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if dimensions == 3:
                point = (i, j, z)
            else:
                point = (i, j, z, w)

            grid[point] = char

    return grid


def generate_neighbors(point: Tuple[int, ...], dimensions: int = 3):
    """Generate all the neighbors of the given 3 or 4 dimensional point."""
    assert dimensions in (3, 4)

    if dimensions == 3:
        x, y, z = point
    else:
        x, y, z, w = point

    for X in (x - 1, x, x + 1):
        for Y in (y - 1, y, y + 1):
            for Z in (z - 1, z, z + 1):
                if dimensions == 3:
                    if (X, Y, Z) != point:
                        yield (X, Y, Z)
                else:
                    for W in (w - 1, w, w + 1):
                        if (X, Y, Z, W) != point:
                            yield (X, Y, Z, W)


def count_active_neighbors(
    grid: Dict[Tuple[int, ...], str], point: Tuple[int, ...], dimensions: int = 3
):
    """Count the active neighbors of the given 3 or 4 dimensional point"""
    assert dimensions in (3, 4)

    return sum(
        1
        for neighbor_point in generate_neighbors(point, dimensions=dimensions)
        if grid.get(neighbor_point, INACTIVE) == ACTIVE
    )


def iterate_simulation(grid: Dict[Tuple[int, ...], str], dimensions: int = 3):
    """Make one pass at the simulation from the starting grid state and return a new grid."""
    assert dimensions in (3, 4)

    new_grid: Dict[Tuple[int, ...], str] = {}

    point: Tuple[int, ...]
    for point in grid.keys():
        for neighbor_point in generate_neighbors(point, dimensions=dimensions):
            state: str = grid.get(neighbor_point, INACTIVE)
            count: int = count_active_neighbors(
                grid, neighbor_point, dimensions=dimensions
            )

            if state == ACTIVE and count in (2, 3):
                # stay the same
                new_grid[neighbor_point] = state
            elif state == INACTIVE and count == 3:
                new_grid[neighbor_point] = ACTIVE
            else:
                new_grid[neighbor_point] = INACTIVE

    return new_grid


if __name__ == "__main__":
    filename: str = sys.argv[1]

    contents: List[str] = [line.strip() for line in open(filename).readlines()]

    grid: Dict[Tuple[int, ...], str] = initialize_grid(contents)

    for cycle in range(CYCLE_LIMIT):
        print(f"3 Dimensions cycle: {cycle}")
        grid = iterate_simulation(grid)

    count = sum(1 for cell in grid.values() if cell == ACTIVE)
    print(f"Part 1 count: {count}")

    grid = initialize_grid(contents, dimensions=4)

    for cycle in range(CYCLE_LIMIT):
        print(f"4 Dimensions cycle: {cycle}")
        grid = iterate_simulation(grid, dimensions=4)

    count = sum(1 for cell in grid.values() if cell == ACTIVE)
    print(f"Part 2 count: {count}")

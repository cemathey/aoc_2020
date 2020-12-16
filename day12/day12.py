import sys
from typing import List, NamedTuple, Sequence, Tuple
from pprint import pprint
import math


class Instruction(NamedTuple):
    instruction: str
    magnitude: int


def build_instructions(lines: List[str]) -> Sequence[Instruction]:
    """Build a list of Instruction named tuples from the provided file contents."""
    instructions = []

    for line in open(filename).readlines():
        instruction = line[0]
        magnitude = int(line[1:])

        instructions.append(Instruction(instruction, magnitude))

    return instructions


def calc_position_change(facing: int, magnitude: int) -> Tuple[int, int]:
    """Calculate the change east/west and north/south for the given facing (degrees) and magnitude"""
    radians: float = math.radians(facing)

    dx: int = int(math.cos(radians)) * magnitude
    dy: int = int(math.sin(radians)) * magnitude

    return (dx, dy)


def wrap_facing(facing: int) -> int:
    """Handle turning past 0 or 360 degrees."""
    return facing % 360


def cardinal_to_degrees(instruction: str) -> int:
    """Turn a cardinal direction into the equivalent degrees."""
    degrees: int

    if instruction == "N":
        degrees = 90
    elif instruction == "E":
        degrees = 0
    elif instruction == "W":
        degrees = 180
    elif instruction == "S":
        degrees = 270

    return degrees


def part_1(
    instructions: Sequence[Instruction],
    facing: int = 0,
    ship_x: int = 0,
    ship_y: int = 0,
):
    """Move and turn the ship given the provided instructions and return the manhattan distance."""
    dx: int = 0
    dy: int = 0

    for instruction, magnitude in instructions:
        dx = dy = 0

        if instruction == "L":
            facing += magnitude
        elif instruction == "R":
            facing -= magnitude
        elif instruction == "F":
            dx, dy = calc_position_change(facing, magnitude)
        # N E S W
        else:
            direction = cardinal_to_degrees(instruction)
            dx, dy = calc_position_change(direction, magnitude)

        ship_x += dx
        ship_y += dy

        # Handle wrapping
        facing = wrap_facing(facing)

    # Manhattan distance
    return abs(ship_x) + abs(ship_y)


def correct_point_signs(quadrant, direction, magnitude, way_x, way_y):
    """Return the adjusted waypoint position based off the starting quadrant and the given rotation."""

    # magnitude can be 90, 180 or 270 based off the input file
    assert magnitude in (90, 180, 270)
    assert quadrant in (1, 2, 3, 4)
    turns = magnitude // 90
    # Turn 1, 2 or 3 times

    if direction == "L":
        # Turning left = increasing quadrant
        quadrant += turns
    else:
        # Turning right = decreasing quadrant
        quadrant -= turns

    # Handle wrapping quadrants
    if quadrant > 4:
        quadrant = abs(4 - quadrant)
    elif quadrant <= 0:
        quadrant = quadrant + 4

    if quadrant == 1:
        way_x = abs(way_x)
        way_y = abs(way_y)
    elif quadrant == 2:
        way_x = -1 * abs(way_x)
        way_y = abs(way_y)
    elif quadrant == 3:
        way_x = -1 * abs(way_x)
        way_y = -1 * abs(way_y)
    elif quadrant == 4:
        way_x = abs(way_x)
        way_y = -1 * abs(way_y)

    return (way_x, way_y)


def find_quadrant(x: int, y: int) -> int:
    """Return the quadrant the given point lies in."""
    quadrant: int = 0

    if x >= 0 and y > 0:
        quadrant = 1
    if x < 0 and y >= 0:
        quadrant = 2
    if x < 0 and y < 0:
        quadrant = 3
    if x > 0 and y < 0:
        quadrant = 4

    return quadrant


def part_2(
    instructions: Sequence[Instruction],
    facing: int = 0,
    ship_x: int = 0,
    ship_y: int = 0,
    way_x: int = 10,
    way_y: int = 1,
):
    # Change in our waypoint's position
    dx: int = 0
    dy: int = 0

    for instruction, magnitude in instructions:
        if instruction in "LR":
            original_quadrant = find_quadrant(way_x, way_y)

            # These rotations swap x and y components
            if magnitude == 90 or magnitude == 270:
                way_x, way_y = way_y, way_x

            way_x, way_y = correct_point_signs(
                original_quadrant, instruction, magnitude, way_x, way_y
            )
        elif instruction == "F":
            # Move the ship towards the waypoint
            ship_x += magnitude * way_x
            ship_y += magnitude * way_y
        # N E S W
        else:
            direction = cardinal_to_degrees(instruction)
            dx, dy = calc_position_change(direction, magnitude)
            way_x += dx
            way_y += dy

    # Manhattan distance
    return abs(ship_x) + abs(ship_y)


if __name__ == "__main__":
    filename = sys.argv[1]

    contents = open(filename).readlines()
    instructions = build_instructions(contents)

    distance = part_1(instructions)
    print(f"{distance=}")
    assert distance == 1603

    distance = part_2(instructions)
    print(f"{distance=}")
    assert distance == 52866

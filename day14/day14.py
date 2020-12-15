import re
import sys
from collections import defaultdict
from typing import List, Sequence, Tuple, DefaultDict


def parse_mask(raw_mask: str) -> Sequence[str]:
    """Return the given mask as a tuple of strings."""
    return tuple(raw_mask.strip())


def parse_instruction(mem_slot, value) -> Tuple[int, int]:
    """Parse out and return the memory address and new value as integers."""
    pattern = re.compile(r"mem\[(\d+)\]")
    address = pattern.match(mem_slot).groups()[0]
    return (int(address), int(value))


def apply_mask(mask: Sequence[str], value: int, rules: Sequence[str]) -> Sequence[str]:
    """Apply the given mask to the value given the provided rules.

    mask: List of characters
    value: Value the mask will be applied to
    rules: Characters to overwrite with the equivalent value from the mask
    """
    bit_length = len(mask)
    binary_value = list(f"{value:0{bit_length}b}")

    for idx, position in enumerate(mask):
        if position in rules:
            binary_value[idx] = position

    return tuple(binary_value)


def generate_combinations(length):
    """Generate all of the binary combinations of the given length"""
    for i in range(2 ** length):
        yield tuple(f"{i:0{length}b}")


def address_combinations(masked_value: Sequence[str], placeholder: str = "X"):
    """Generate all of the possible address combinations for each floating value in the mask"""
    placeholder_indexes = [
        idx for idx, char in enumerate(masked_value) if char == placeholder
    ]
    count = len(placeholder_indexes)

    for combo in generate_combinations(count):
        value = list(masked_value)
        for idx, char in zip(placeholder_indexes, combo):
            value[idx] = char
        yield tuple(value)


def value_to_int(binary_list: Sequence[str]) -> int:
    """Convert the given binary sequence to an integer."""
    return int("".join(binary_list), base=2)


def run_program(lines: List[str], mask_values: bool = True) -> int:
    """Run the program masking either the values or memory addresses.
    lines: either a new mask or a memory address/new value
    mask_values: True: Mask the new values
    mask_values: False: Mask the memory address

    return: Sum of all values in memory
    """

    # Only track memory locations that are updated, defaults to 0
    memory: DefaultDict[int, int] = defaultdict(int)

    for line in lines:
        parts: List[str] = line.strip().split(" = ")
        left, right = parts

        if left == "mask":
            mask = parse_mask(right)
        else:
            address, value = parse_instruction(left, right)

            # Part 1
            if mask_values:
                binary_value: Sequence[str] = apply_mask(mask, value, "01")
                memory[address] = value_to_int(binary_value)
            # Part 2
            else:
                binary_address: Sequence[str] = apply_mask(mask, address, "1X")
                for address_combo in address_combinations(binary_address):
                    memory[value_to_int(address_combo)] = value

    return sum(value for value in memory.values())


if __name__ == "__main__":
    filename = sys.argv[1]

    program = open(filename).readlines()

    total = run_program(program, mask_values=True)
    print(f"Part 1: {total=}")

    total = run_program(program, mask_values=False)
    print(f"Part 2: {total=}")

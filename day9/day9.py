from itertools import combinations
import sys
from typing import List, Tuple, Sequence


def build_xmas_list(filename: str) -> List[int]:
    """Read the instructions from the provided file."""
    xmas_values = [int(line) for line in open(filename).readlines()]

    return xmas_values


def find_invalid_value(values: Sequence[int], preamble_len: int = 25) -> int:
    """Return the first value we find that cannot be expressed as the sum of two
    unique integers in the previous preamble_len numbers"""
    valid_value: bool = True
    start_idx: int = 0
    chunk_len: int = preamble_len

    while valid_value:
        next_value = values[chunk_len]

        # Use a set to consider only unique number pairs
        summands = set(values[start_idx:chunk_len])

        # Generate all of the potential summand combinations of length 2
        potential_combinations = combinations(summands, 2)

        for x, y in potential_combinations:
            if next_value == (x + y):
                break
        else:
            # Loop has been exhausted without finding a valid pair of numbers adding up to next_value
            valid_value = False
            break

        start_idx += 1
        chunk_len += 1

    return next_value


def find_encryption_weakness(values: Sequence[int], invalid_value: int) -> int:
    """Find the encryption weakness given our sequence of values and an already calculated invalid_value"""

    invalid_value_idx: int = values.index(invalid_value)
    start_idx: int = -1
    not_found: bool = True

    while not_found:
        start_idx += 1

        cumulative_sum: int = 0
        stop_idx: int = invalid_value_idx

        sliding_region: Sequence[int] = values[start_idx:stop_idx]

        for (idx_offset, num) in enumerate(sliding_region):
            cumulative_sum += num

            if cumulative_sum > invalid_value:
                break
            elif cumulative_sum == invalid_value:
                # our index within our sliding region needs to be adjusted to account for the distance from the start
                stop_idx = start_idx + idx_offset + 1
                not_found = False
                break

    target_region: Sequence[int] = values[start_idx:stop_idx]
    return min(target_region) + max(target_region)


if __name__ == "__main__":
    filename: str = sys.argv[1]

    preamble_len: int = int(sys.argv[2])
    xmas_values: List[int] = build_xmas_list(filename)

    invalid_value: int = find_invalid_value(xmas_values, preamble_len)
    weakness: int = find_encryption_weakness(xmas_values, invalid_value)

    print(f"Part 1: {invalid_value}")
    print(f"Part 2: {weakness}")
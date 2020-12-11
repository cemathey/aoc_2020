import sys
from collections import Counter
from typing import List, Sequence, Tuple

if __name__ == "__main__":
    filename: str = sys.argv[1]

    # Snag our joltages from the file and prepend our charging outlet joltage
    joltages: List[int] = [0] + [int(voltage) for voltage in open(filename).readlines()]

    # Our built in device joltage is 3 higher than the highest joltage in our collection of adaptors
    built_in: int = max(joltages) + 3
    joltages.append(built_in)

    joltages = sorted(joltages)

    # List of differences of each pair of joltages
    differences: List[int] = [b - a for a, b in zip(joltages, joltages[1:])]
    difference_count: Counter = Counter(differences)

    print(
        f"Part 1: 1 jolt: {difference_count[1]} * 3 jolt: {difference_count[3]} = {difference_count[1] * difference_count[3]}"
    )

    current_length: int = 1
    region_sizes: List[int] = []
    for previous, current in zip(differences, differences[1:]):
        if previous == current:
            current_length += 1
        else:
            # We only care about groups of 1 joltage difference that are longer than 1
            if previous == 1 and current_length > 1:
                region_sizes.append(current_length)
            current_length = 1

    region_count: Counter = Counter(region_sizes)

    # Combinations for regions of length 2, 3 and 4 respectively
    possible_combinations: Sequence[int] = (2, 4, 7)
    keys: List[int] = sorted(region_count.keys())

    total_combinations: int = 1
    for combo, key in zip(possible_combinations, keys):
        total_combinations *= combo ** region_count[key]

    print(f"Part 2: {total_combinations} combinations of joltage adaptors.")

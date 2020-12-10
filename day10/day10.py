import sys
from itertools import tee
from functools import reduce
from collections import Counter, defaultdict
from pprint import pprint
from typing import Dict

if __name__ == "__main__":
    filename: str = sys.argv[1]

    # Snag our joltages from the file and prepend our charging outlet joltage
    joltages = [0] + [int(voltage) for voltage in open(filename).readlines()]

    # Our built in device joltage is 3 higher than the highest joltage in our collection of adaptors
    built_in = max(joltages) + 3
    joltages.append(built_in)

    joltages = sorted(joltages)

    # List of differences of each pair of joltages
    differences = [b - a for a, b in zip(joltages, joltages[1:])]

    count = Counter(differences)

    print(f"1 jolt: {count[1]} * 3 jolt: {count[3]} = {count[1] * count[3]}")

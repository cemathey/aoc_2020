import sys
from typing import NamedTuple, Dict, List, Tuple
import string
from pprint import pprint
from collections import Counter

EMPTY_BAG: str = "no other bags"


class Bag(NamedTuple):
    color: str
    qty: int


def sum_bags(starting_from: str, bag_rules: Dict[str, Tuple[Bag]]):
    """Recursively sum the number of bags contained by the given starting_from bag"""
    bag_sum = 0
    for color, qty in bag_rules[starting_from]:
        bag_sum += qty + qty * sum_bags(color, bag_rules)

    return bag_sum


def can_contain_bag(
    key: str, starting_from: str, bag_rules: Dict[str, Tuple[Bag]], found: bool = False
) -> bool:
    """Recursively search bag_rules for the given key and return True if at any point it can contain that bag"""

    # found: bool = False
    # Rely on python only initializing default function arguments once

    for color, qty in bag_rules[starting_from]:
        if key == color:
            return True
        else:
            found = can_contain_bag(key, color, bag_rules, found)

    return found


if __name__ == "__main__":
    filename: str = sys.argv[1]
    bag_rules: Dict[str, Tuple[Bag]] = dict()
    target_bag: str = "shiny gold bag"

    for line in open(filename).readlines():
        line = line.strip()[:-1]  # Remove periods

        # Line pattern: <color> contain <qty> <color>, ...
        bag, children = line.split("contain")

        # Almost certainly slower but more readable than slicing off the end of strings
        # Make the bag name singular
        bag = bag.strip().replace("bags", "bag")

        bags = []
        # Will still return a one element list even if `,` isn't found
        for child in children.split(","):
            child = child.strip()
            if child != EMPTY_BAG:
                # Split on the first whitespace to get the quantity and color
                num_idx: int = child.find(" ")
                quantity: int = int(child[0:num_idx])
                color: str = child[num_idx + 1 :]
                bags.append(Bag(qty=quantity, color=color.replace("bags", "bag")))

        bag_rules[bag] = tuple(bags)

    # Iterate through all of the bag rules and count the number that can contain our target bag.
    contains_bag = sum(
        can_contain_bag(target_bag, starting_from, bag_rules)
        for starting_from in bag_rules.keys()
    )

    print(f"Part 1: {contains_bag} bags can contain {target_bag}")
    print(f"Part 2: {target_bag} contains {sum_bags(target_bag, bag_rules)} bags.")

import sys
from typing import NamedTuple, Tuple, List, Dict, Set


class Food(NamedTuple):
    ingredients: Tuple[str, ...]
    allergens: Tuple[str, ...]


def parse_food(line: str) -> Food:
    """Return a valid Food from the given line."""
    left, right = line.strip().split(" (contains ")

    foods: List[str] = [food for food in left.split(" ")]

    # Slice off everything except the ending parentheses
    allergens: List[str] = [allergen for allergen in right[:-1].split(", ")]

    return Food(tuple(foods), tuple(allergens))


def collect_foods_allergen(foods: Tuple[Food, ...], allergen: str) -> Tuple[Food, ...]:
    """Return a tuple of all foods that contain the given allergen."""
    return tuple(food for food in foods if allergen in food.allergens)


def collect_foods_ingredient(
    foods: Tuple[Food, ...], ingredient: str
) -> Tuple[Food, ...]:
    """Return a tuple of all foods that contain the given ingredient."""
    return tuple(food for food in foods if ingredient in food.ingredients)


def collect_unknown_ingredients(
    decoded_allergens: Dict[str, str], foods: Tuple[Food, ...], allergen: str
):
    """Collect all of the unknown ingredients for each food that contains the given allergen."""
    unique_ingredients: List[List[str]] = []
    for food in foods:
        filtered_ingredients: List[str] = []
        for ingredient in food.ingredients:
            if (
                allergen in food.allergens
                and ingredient not in decoded_allergens.values()
            ):
                filtered_ingredients.append(ingredient)
        # No empty lists
        if filtered_ingredients:
            unique_ingredients.append(filtered_ingredients)

    return unique_ingredients


def decode_allergens(foods: Tuple[Food, ...]) -> Dict[str, str]:
    """Populate our decoded allergens by searching for foods that contain an allergen and exactly 1 unknown ingredient."""
    allergens: Set[str] = set(allergen for food in foods for allergen in food.allergens)

    decoded_allergens: Dict[str, str] = {}

    # To decode our allergens, iterate through the allergens until we can find a set intersection of ingredients for that allergen that has exactly one commonality
    while len(decoded_allergens) < len(allergens):
        for allergen in allergens:
            unknown_ingredients: List[List[str]] = collect_unknown_ingredients(
                decoded_allergens, foods, allergen
            )

            # Can't pass a generator expression, make a tuple of sets and then explode it
            intersecting_ingredients = set.intersection(
                *tuple(set(ingredients) for ingredients in unknown_ingredients)
            )

            if len(intersecting_ingredients) == 1:
                decoded_allergens[allergen] = intersecting_ingredients.pop()

    return decoded_allergens


if __name__ == "__main__":
    filename = sys.argv[1]

    contents = open(filename).readlines()

    foods: Tuple[Food, ...] = tuple(parse_food(line) for line in contents)
    decoded_allergens: Dict[str, str] = decode_allergens(foods)
    answer: int = sum(
        1
        for food in foods
        for ingredient in food.ingredients
        if ingredient not in decoded_allergens.values()
    )

    dangerous_ingredients: str = ",".join(
        v for k, v in sorted(decoded_allergens.items())
    )
    print(f"Part 1: answer= {answer}")
    print(f"Part 2: dangerous_ingredients= {dangerous_ingredients}")
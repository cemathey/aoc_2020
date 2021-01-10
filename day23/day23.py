import sys
from typing import Deque, Tuple
from collections import deque


def pickup_cups(
    cups: Tuple[int, ...], current_cup_idx: int, qty: int = 3
) -> Tuple[int, ...]:
    picked_up = []
    for _ in range(qty):
        current_cup_idx += 1
        if current_cup_idx >= len(cups):
            current_cup_idx = 0
        grabbed = cups[current_cup_idx]
        picked_up.append(grabbed)

    return tuple(picked_up)


def grab_destination_cup(
    cups: Tuple[int, ...], current_cup: int, picked_up_cups: Tuple[int, ...]
) -> int:
    destination_cup: int = current_cup - 1

    smallest: int = min(cups)
    largest: int = max(cups)

    if destination_cup < smallest:
        destination_cup = largest

    while destination_cup in picked_up_cups:
        destination_cup -= 1

        if destination_cup < smallest:
            destination_cup = largest

    return destination_cup


def place_cups(
    cups: Tuple[int, ...], destination_cup: int, picked_up_cups: Tuple[int, ...]
) -> Tuple[int, ...]:
    """"""
    temp_cups = list(cups)
    for remove in picked_up_cups:
        temp_cups.remove(remove)
    new_cups = []
    destination_cup_idx = temp_cups.index(destination_cup)

    new_cups.extend(temp_cups[0 : destination_cup_idx + 1])
    new_cups.extend(picked_up_cups)
    new_cups.extend(temp_cups[destination_cup_idx + 1 :])

    return tuple(new_cups)


def make_move(cups: Tuple[int, ...], current_cup_idx: int = 0):
    current_cup = cups[current_cup_idx]
    picked_up_cups = pickup_cups(cups, current_cup_idx)
    destination_cup = grab_destination_cup(cups, current_cup, picked_up_cups)
    new_cups = place_cups(cups, destination_cup, picked_up_cups)

    return new_cups


def make_n_moves(moves: 10, cups):
    current_cup_idx = 0

    for _ in range(1, moves + 1):
        cups = make_move(cups, current_cup_idx)
        current_cup_idx += 1
        if current_cup_idx >= len(cups):
            current_cup_idx = 0

    return cups


if __name__ == "__main__":
    cups = list(int(cup) for cup in "389125467")

    current_cup_idx = 0

    new_cups = make_n_moves(10, cups)

    #     *
    # 3 2 5 4 6 7 8 9 1
    # 3 2 5 8 9 1
    # 7 2 5 8 9 1 3 4 6

    print(f"{cups=}")
    print(f"{new_cups=}")
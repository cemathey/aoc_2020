import sys
from collections import defaultdict
from typing import Sequence


def counting_game(starting_numbers: Sequence[int], stop_turn) -> int:

    memory = defaultdict(lambda: (0, 0))

    # Preload the memory with the starting numbers
    turns = [turn for turn in range(1, len(starting_numbers) + 1)]
    for num, turn in zip(starting_numbers, turns):
        memory[num] = (turn, 0)

    # Update the turn based on how many starting numbers we have
    turn = turns[-1] + 1
    last_spoken = starting_numbers[-1]
    while turn <= stop_turn:

        curr_turn, prev_turn = memory[last_spoken]

        if prev_turn == 0:
            # Respond 0 the first time a number is spoken
            answer = 0
        else:
            # Respond with the difference of the last two times the number was spoken
            answer = curr_turn - prev_turn

        # answer was spoken, update the last times it was spoken
        curr_turn, prev_turn = memory[answer]
        memory[answer] = (turn, curr_turn)

        last_spoken = answer

        turn += 1

    return answer


if __name__ == "__main__":
    filename = sys.argv[1]

    numbers = [int(num) for num in open(filename).read().split(",")]

    # assert counting_game([0, 3, 6], 2020) == 436
    # assert counting_game([1, 3, 2], 2020) == 1
    # assert counting_game([2, 1, 3], 2020) == 10
    # assert counting_game([1, 2, 3], 2020) == 27
    # assert counting_game([2, 3, 1], 2020) == 78
    # assert counting_game([3, 2, 1], 2020) == 438
    # assert counting_game([3, 1, 2], 2020) == 1836

    # assert counting_game([0, 3, 6], 30000000) == 175594

    answer = counting_game(numbers, 2020)
    print(f"Part 1: {answer}")

    answer = counting_game(numbers, 30000000)
    print(f"Part 2: {answer}")

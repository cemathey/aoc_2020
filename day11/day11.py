import sys
from typing import List, Tuple, Sequence, Callable
from functools import reduce
from copy import deepcopy

FLOOR: str = "."
EMPTY: str = "L"
OCCUPIED: str = "#"


def part1_conditions(seat: str, adjacent_occupied: int):
    """Rules to satisfy when to change a seat for part 1."""
    if seat == EMPTY and adjacent_occupied == 0:
        return OCCUPIED
    elif seat == OCCUPIED and adjacent_occupied >= 4:
        return EMPTY
    else:
        return seat


def part2_conditions(seat: str, adjacent_occupied: int):
    """Rules to satisfy when to change a seat for part 2."""
    if seat == EMPTY and adjacent_occupied == 0:
        return OCCUPIED
    elif seat == OCCUPIED and adjacent_occupied >= 5:
        return EMPTY
    else:
        return seat


def count_occupied_seats(
    board: List[List[str]], row: int, col: int, adjacent_only: bool
) -> int:
    """Count either the number of adjacent seats that are filled, or the number of visible seats that are filled."""

    # Offset functions to adjust the row/col indexes to check the appropriate parts of the board
    index_adjustments = [
        lambda row, col: (row, col + 1),
        lambda row, col: (row, col - 1),
        lambda row, col: (row + 1, col),
        lambda row, col: (row - 1, col),
        lambda row, col: (row - 1, col - 1),
        lambda row, col: (row - 1, col + 1),
        lambda row, col: (row + 1, col - 1),
        lambda row, col: (row + 1, col + 1),
    ]

    # None of our rows are sparse so we only need to check one
    max_row: int = len(board)
    max_col: int = len(board[0])

    total: int = 0
    for adjust_index in index_adjustments:
        adj_row, adj_col = adjust_index(row, col)

        if adjacent_only:
            if 0 <= adj_row < max_row and 0 <= adj_col < max_col:
                if board[adj_row][adj_col] == OCCUPIED:
                    total += 1
        else:
            # Check every square that we can see (until we hit a chair, occupied or otherwise) in each of the 8 directions
            while 0 <= adj_row < max_row and 0 <= adj_col < max_col:
                if board[adj_row][adj_col] == OCCUPIED:
                    total += 1
                    break
                elif board[adj_row][adj_col] == EMPTY:
                    break
                adj_row, adj_col = adjust_index(adj_row, adj_col)

    return total


def read_board(filename: str) -> List[List[str]]:
    lines = open(filename).readlines()
    board = [list(line.strip()) for line in lines]

    return board


def run_simulation(
    board: List[List[str]],
    update_condition: Callable,
    count_callback: Callable,
    adjacent_only=True,
) -> int:
    """Update the board until it stops changing state and return the number of occupied seats at that point."""
    current_board = deepcopy(board)
    previous_board = deepcopy(board)

    board_changing = True
    while board_changing:
        for i, row in enumerate(current_board):
            for j, seat in enumerate(row):
                # Every person makes their decision simultaneously so we have to compare against the previous board state
                adjacent_occupied = count_occupied_seats(
                    previous_board, i, j, adjacent_only
                )

                current_board[i][j] = update_condition(seat, adjacent_occupied)

        if current_board == previous_board:
            board_changing = False

        previous_board = deepcopy(current_board)

    total = reduce(lambda total, row: total + row.count(OCCUPIED), current_board, 0)

    return total


if __name__ == "__main__":
    filename = sys.argv[1]
    board = read_board(filename)

    occupied_seats = run_simulation(
        board, part1_conditions, count_occupied_seats, adjacent_only=True
    )
    print(f"Part 1: {occupied_seats}")

    occupied_seats = run_simulation(
        board, part2_conditions, count_occupied_seats, adjacent_only=False
    )
    print(f"Part 2: {occupied_seats}")
from typing import NamedTuple, List, Tuple, Callable, Dict
from pprint import pprint
from itertools import cycle
import sys


class Instruction(NamedTuple):
    operation: str
    argument: int


def program_terminates_correctly(instructions: Tuple[Instruction]) -> Tuple[bool, int]:
    """Run a set of instructions and determine whether it terminates by infinite loop or correctly"""
    visited_instruction_idxs: Dict[int, bool] = dict(
        (idx, False) for idx in range(len(instructions))
    )

    accumulator: int = 0
    instruction_pointer: int = 0

    while True:

        # Instruction pointer falls off the end of our instruction list
        if instruction_pointer == len(instructions):
            return (True, accumulator)

        # Infinite loop
        if visited_instruction_idxs[instruction_pointer]:
            return (False, accumulator)

        visited_instruction_idxs[instruction_pointer] = True

        instruction = instructions[instruction_pointer]
        accumulator, instruction_pointer = process_instruction(
            instruction, accumulator, instruction_pointer
        )


def process_instruction(
    instruction: Instruction, accumulator: int = 0, instruction_pointer: int = 0
) -> Tuple[int, int]:
    """Process an individual instruction and return the updated accumulator and instruction_pointer"""
    operation, argument = instruction

    if operation == "acc":
        accumulator += argument
        instruction_pointer += 1
    elif operation == "nop":
        instruction_pointer += 1
    elif operation == "jmp":
        instruction_pointer += argument

    return accumulator, instruction_pointer


def invert_instruction(instruction: Instruction) -> Instruction:
    """Turn a nop into a jmp and vice versa"""
    operation, argument = instruction

    if operation == "nop":
        new_instruction = Instruction("jmp", argument)
    elif operation == "jmp":
        new_instruction = Instruction("nop", argument)

    return new_instruction


def build_initial_instructions(filename: str) -> List[Instruction]:
    """Read the instructions from the provided file."""
    instructions = []
    for line in open(filename).readlines():
        opp, arg = line.split(" ")
        instructions.append(Instruction(opp, int(arg)))

    return instructions


def build_instruction_combinations(
    instructions: List[Instruction],
) -> List[Tuple[Instruction]]:
    """Generate all of the different possible instruction combinations by inverting a single nop/jmp operation"""

    # Find the indexes of every instruction we'll attempt to modify
    modifiable_instruction_idxs = [
        idx
        for idx, instruction in enumerate(instructions)
        if instruction.operation in ("nop", "jmp")
    ]

    instruction_combinations = []
    # Keep the original program as the first combination to test
    instruction_combinations.append(tuple(instructions))

    for idx in modifiable_instruction_idxs:
        temp_instructions = instructions.copy()
        instruction = instructions[idx]

        temp_instructions[idx] = invert_instruction(instruction)
        instruction_combinations.append(tuple(temp_instructions))

    return instruction_combinations


if __name__ == "__main__":
    filename: str = sys.argv[1]
    instructions = build_initial_instructions(filename)

    accumulator: int = 0
    terminates_correctly: bool = False
    instruction_combinations = build_instruction_combinations(instructions)

    terminates_correctly, accumulator = program_terminates_correctly(
        instruction_combinations[0]
    )
    print(f"Part 1: {accumulator=}")

    for combination in instruction_combinations:
        terminates_correctly, accumulator = program_terminates_correctly(combination)

        if terminates_correctly:
            break

    print(f"Part 2: {accumulator=}")

import sys
from itertools import count


def transform_subject_number(starting_value, subject_number=7, divisor=20201227):
    """Transform the starting_value with the given subject_number and divisor."""
    starting_value *= subject_number
    starting_value %= divisor

    return starting_value


def deduce_loop_size(public_key):
    """Figure out what loop size will produce the given public key."""
    test_subject_number = 1
    for loop_size in count(1):
        test_subject_number = transform_subject_number(test_subject_number)
        if test_subject_number == public_key:
            return loop_size


def calc_private_key(loop_size, public_key):
    """Transform the given public_key loop_size times to produce the private key"""
    starting_value = 1
    for _ in range(loop_size):
        starting_value = transform_subject_number(starting_value, public_key)

    return starting_value


if __name__ == "__main__":
    filename = sys.argv[1]
    keys = open(filename).readlines()

    card_pub_key = int(keys[0])
    door_pub_key = int(keys[1])

    card_loop_size = deduce_loop_size(card_pub_key)
    door_loop_size = deduce_loop_size(door_pub_key)

    card_priv_key = calc_private_key(door_loop_size, card_pub_key)
    door_priv_key = calc_private_key(card_loop_size, door_pub_key)

    print(f"card_priv_key={card_priv_key} door_priv_key={door_priv_key}")
import sys
from typing import NamedTuple, List, Sequence, Generator, Dict
from pprint import pprint
from collections import defaultdict


class TicketField(NamedTuple):
    name: str
    ranges: Sequence[Sequence[int]]


def build_ticket_fields(fields: str) -> Sequence[TicketField]:
    """Build a TicketField object for every provided field."""
    ticket_fields = []

    for line in fields.splitlines():
        field_name, raw_ranges = line.split(": ")
        temp_ranges = []
        for raw_range in raw_ranges.split(" or "):
            lower, upper = raw_range.split("-")
            temp_ranges.append((int(lower), int(upper)))

        ranges = tuple(temp_ranges)

        ticket_fields.append(TicketField(name=field_name, ranges=ranges))

    return tuple(ticket_fields)


def parse_tickets(raw_tickets: str) -> Generator:
    """Yield a ticket (tuple of integers) for every ticket contained in raw_tickets"""

    # Grab every ticket but skip the section header
    for line in raw_tickets.split("\n")[1:]:
        yield tuple(int(num) for num in line.split(","))


def field_in_range(ticket_field: TicketField, field_value: int) -> bool:
    """Test whether the given field_value is within limits for the given ticket_field"""
    return any(lower <= field_value <= upper for lower, upper in ticket_field.ranges)


def valid_field(ticket_fields: Sequence[TicketField], field_value: int) -> bool:
    """Check the given field value against the rules for every ticket field"""
    return any(
        field_in_range(ticket_field, field_value) for ticket_field in ticket_fields
    )


def valid_ticket(ticket_fields: Sequence[TicketField], ticket: Sequence[int]) -> bool:
    """Test whether every field for the given ticket is valid."""
    return all(valid_field(ticket_fields, field) for field in ticket)


def collect_invalid_fields(
    ticket_fields: Sequence[TicketField], nearby_tickets: Sequence[Sequence[int]]
) -> Generator:
    """Scan every field for each ticket in nearby_tickets and yield each field value that is invalid for all fields in ticket_fields."""

    for ticket in nearby_tickets:
        for field in ticket:
            if not valid_field(ticket_fields, field):
                yield field


def build_truth_table(
    ticket_fields: Sequence[TicketField], valid_tickets: Sequence[Sequence[int]]
):
    """Populate and return a 3D truth table (position, field_index, validity) for our given ticket_fields and valid_tickets"""

    # 3D array, i=position j=field index in ticket_fields
    num_positions = len(valid_tickets[0])
    num_fields = len(ticket_fields)

    truth_table = [[list() for j in range(num_fields)] for i in range(num_positions)]

    for ticket in valid_tickets:
        for position, field_value in enumerate(ticket):
            for field_idx, ticket_field in enumerate(ticket_fields):
                validity = field_in_range(ticket_field, field_value)

                truth_table[position][field_idx].append(validity)

    return truth_table


def find_possible_fields(truth_table):
    """Iterate through the truth table and yield """
    for position, fields in enumerate(truth_table):
        all_true = [all(values) for values in fields]
        if all_true.count(True) == 1:
            key_field = all_true.index(True)
            yield key_field, position

    return None


def deduce_truth_table(truth_table, ticket_fields):
    deduced_fields = set()
    num_positions = len(truth_table)
    field_names = [ticket_field.name for ticket_field in ticket_fields]
    ordered_field_names = [None] * len(field_names)

    while len(deduced_fields) < num_positions:
        # key_field_idx is the index of the field_name i.e. 0 = class 1 = row 2 = seat
        for key_field_idx, position in find_possible_fields(truth_table):
            field_name = field_names[key_field_idx]
            deduced_fields.add(field_name)
            ordered_field_names[position] = field_name

            # Having found what field this position is, set every other field for this position to not possible
            for field_idx, fields in enumerate(truth_table[position]):
                if field_idx != key_field_idx:
                    truth_table[position][field_idx] = [False] * num_positions

            # Having found what field this position is, set that field for every other position to not possible
            for idx, fields in enumerate(truth_table):
                if idx != position:
                    truth_table[idx][key_field_idx] = [False] * num_positions

    return ordered_field_names


if __name__ == "__main__":
    filename = sys.argv[1]

    contents = open(filename).read()

    parts = contents.split("\n\n")
    _fields, _my_ticket, _nearby_tickets = parts

    ticket_fields = build_ticket_fields(_fields)
    my_ticket = next(parse_tickets(_my_ticket))
    nearby_tickets = tuple(ticket for ticket in parse_tickets(_nearby_tickets))

    total = sum(
        field for field in collect_invalid_fields(ticket_fields, nearby_tickets)
    )

    print(f"Part 1 ticket scanning error rate is: {total}")

    valid_nearby_tickets = [
        ticket for ticket in nearby_tickets if valid_ticket(ticket_fields, ticket)
    ]

    truth_table = build_truth_table(ticket_fields, valid_nearby_tickets)
    ordered_field_names = deduce_truth_table(truth_table, ticket_fields)

    total = 1
    for position, field_name in enumerate(ordered_field_names):
        if "departure" in field_name:
            total *= my_ticket[position]

    # total=360952328957119 too high
    # total=2016493457861 too low

    print(f"Part 2 total: {total}")
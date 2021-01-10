import sys
from typing import NamedTuple, List, Sequence, Generator, Dict
from pprint import pprint
from collections import defaultdict


class TicketField:
    def __init__(self, field_name, ranges):
        self.field_name = field_name
        self.ranges = ranges

    @property
    def ranges(self):
        return self._ranges

    @ranges.setter
    def ranges(self, raw_ranges):
        """Parse the given collection of valid ranges for the field."""
        temp_ranges = []

        for _range in raw_ranges.split(" or "):
            lower, upper = _range.split("-")
            lower = int(lower)
            upper = int(upper)
            temp_ranges.append((lower, upper))

        self._ranges = tuple(temp_ranges)

    def __contains__(self, value: int) -> bool:
        """Test whether the given value meets the conditions for this field."""
        contains: bool = False

        for lower, upper in self.ranges:
            if lower <= value <= upper:
                return True

        return contains

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.field_name=} {self.ranges=}>"


def build_ticket_fields(fields: str) -> Sequence[TicketField]:
    """Build a TicketField object for every provided field."""
    ticket_fields = []
    for line in fields.splitlines():
        field_name, ranges = line.split(": ")
        field = TicketField(field_name, ranges)
        ticket_fields.append(field)

    return tuple(ticket_fields)


def parse_tickets(raw_tickets: str) -> Generator:
    """Yield a ticket (tuple of integers) for every ticket contained in raw_tickets"""

    # Grab every ticket but skip the section header
    for line in raw_tickets.split("\n")[1:]:
        yield tuple(int(num) for num in line.split(","))


def valid_field(ticket_fields: Sequence[TicketField], field_value: int) -> bool:
    """Check the given field value against all valid field values"""
    return any(field_value in ticket_field for ticket_field in ticket_fields)


def find_invalid_fields(
    ticket_fields: Sequence[TicketField], nearby_tickets: Sequence[Sequence[int]]
) -> Generator:
    """Scan every field for each ticket in nearby_tickets and yield each invalid field value."""

    for ticket in nearby_tickets:
        for field in ticket:
            if not valid_field(ticket_fields, field):
                yield field


def valid_ticket(ticket_fields: Sequence[TicketField], ticket: Sequence[int]) -> bool:
    """Test whether every field for the given ticket is valid."""

    return all(valid_field(ticket_fields, field) for field in ticket)


def build_truth_table(
    ticket_fields: Sequence[TicketField], valid_tickets: Sequence[Sequence[int]]
):

    # defaultdict[int, defaultdict[str, list]]
    truth_table = defaultdict(lambda: defaultdict(list))

    for ticket_field in ticket_fields:
        for ticket in valid_tickets:
            for position, field_value in enumerate(ticket):
                valid = field_value in ticket_field
                field_name = ticket_field.field_name
                truth_table[position][field_name].append(valid)

    return truth_table


def find_only_possible_field(fields):
    key_field = None

    all_true = [all(values) for values in fields.values()]
    if all_true.count(True) == 1:
        field_names = [field_name for field_name in fields.keys()]
        key_field = field_names[all_true.index(True)]

    return key_field


def reduce_truth_table(truth_table):
    """Continously update our truth table of positions and field names until until there is only one valid choice for every position."""
    ambiguity_remains: bool = True
    updated_fields = []

    while ambiguity_remains:

        key_field = None
        # Find a position that has one and only one field that is all True
        for position, fields in truth_table.items():
            key_field = find_only_possible_field(fields)
            if key_field and key_field not in updated_fields:
                updated_fields.append(key_field)

                # For our position, update every other field to False since they're not possible
                field_count = len(truth_table[position][key_field])

                for field_name, values in truth_table[position].items():
                    if field_name != key_field:
                        truth_table[position][field_name] = [False] * field_count

                # For every other position, update the key field to False since they're not possible
                for _pos, fields in truth_table.items():
                    if _pos != position:
                        truth_table[_pos][key_field] = [False] * field_count

            else:
                ambiguity_remains = False


if __name__ == "__main__":
    filename = sys.argv[1]

    contents = open(filename).read()

    parts = contents.split("\n\n")
    _fields, _my_ticket, _nearby_tickets = parts

    ticket_fields = build_ticket_fields(_fields)
    my_ticket = next(parse_tickets(_my_ticket))
    nearby_tickets = tuple(ticket for ticket in parse_tickets(_nearby_tickets))

    total = sum(field for field in find_invalid_fields(ticket_fields, nearby_tickets))

    print(f"Part 1 ticket scanning error rate is: {total}")

    valid_nearby_tickets = [
        ticket for ticket in nearby_tickets if valid_ticket(ticket_fields, ticket)
    ]

    truth_table = build_truth_table(ticket_fields, valid_nearby_tickets)
    reduce_truth_table(truth_table)

    ordered_field_names = []

    for position, fields in truth_table.items():
        for field_name, values in fields.items():
            if True in values and field_name not in ordered_field_names:
                ordered_field_names.append(field_name)

    total = 1

    print(ordered_field_names)

    for idx, field_value in enumerate(my_ticket):
        test = ordered_field_names[idx]
        if "departure" in ordered_field_names[idx]:
            total *= field_value

    # total=360952328957119 too high
    # total=2016493457861 too low

    print(f"Part 2 {total=}")
from utils import read_data
from math import prod
from typing import NamedTuple, List, Set, Dict, Tuple, FrozenSet


class Constraint(NamedTuple):
    name: str
    valid_values: frozenset

    def validate(self, value):
        return value in self.valid_values

    def __repr__(self):
        return f'Constraint(name="{self.name}", valid_values="{self.valid_values}")'


def ingest_constraints(raw_constraints: str) -> List[Constraint]:
    all_constraints = []
    for constraint in raw_constraints.split("\n"):
        # Example line:
        # departure location: 42-570 or 579-960
        name, ranges = constraint.split(": ")
        ranges = ranges.split(" or ")
        valid_numbers = set()
        for constraint_range in ranges:
            low, high = (int(x) for x in constraint_range.split("-"))
            valid_numbers.update(range(low, high+1))
        all_constraints.append(Constraint(name=name, valid_values=frozenset(valid_numbers)))
    return all_constraints


def ingest_tickets(ticket_list: List[str]) -> List[List[int]]:
    all_tickets = []
    for ticket in ticket_list:
        # Discard the label line
        if ticket.endswith(":"):
            continue
        all_tickets.append([int(x) for x in ticket.split(",")])
    return all_tickets


def ingest_input(raw_input: str) -> Tuple[List[Constraint], List[int], List[List[int]]]:
    # Convenience method to completely process raw input into constraints, your ticket, and nearby tickets
    raw_constraints, raw_your_ticket, raw_nearby_tickets = raw_input.split("\n\n")
    constraints = ingest_constraints(raw_constraints)
    your_ticket = ingest_tickets(raw_your_ticket.split("\n"))[0]
    nearby_tickets = ingest_tickets(raw_nearby_tickets.split("\n"))
    return constraints, your_ticket, nearby_tickets


def validate_ticket_part_one(all_valid_values: FrozenSet[int], ticket: List[int]) -> int:
    # Filter the values in the ticket down to just the invalid ones, then sum them
    return sum([value for value in ticket if value not in all_valid_values])


def is_valid_ticket(all_valid_values: FrozenSet[int], ticket: List[int]) -> bool:
    return all(value in all_valid_values for value in ticket)


def get_possible_fields(constraints: List[Constraint], values: List[int]) -> Set[Constraint]:
    return {constraint for constraint in constraints if all(constraint.validate(x) for x in values)}


def map_fields(constraints: List[Constraint], nearby_tickets: List[List[int]]) -> Dict[int, str]:
    ticket_length = len(nearby_tickets[0])
    # Get the set of possible constraints that go with each index
    possible_fields = {i: get_possible_fields(constraints, [x[i] for x in nearby_tickets])
                       for i in range(ticket_length)}

    # Sort by the length of the sets so we can consistently pop the shortest set
    sorted_fields = sorted(possible_fields.items(), key=lambda x: len(x[1]))
    # Now that we've sorted, build our index-to-name mapping piece by piece
    solved_values = dict()
    for i, valid_fields in sorted_fields:
        assert len(valid_fields) == 1, "Must have exactly one field to solve"
        final_constraint = valid_fields.pop()
        # Associate the name with the proper index in our solution
        solved_values[i] = final_constraint.name
        # Remove the constraint as a possibility from all other indices now that we've solved it
        for _, possibilities in sorted_fields:
            possibilities.discard(final_constraint)
    return solved_values


def part_one(constraints: List[Constraint], nearby_tickets: List[List[int]]) -> int:
    # Put all of the constraints together into one big valid-values pile
    valid_values = frozenset.union(*(x.valid_values for x in constraints))
    return sum(validate_ticket_part_one(valid_values, ticket) for ticket in nearby_tickets)


def part_two(constraints: List[Constraint], your_ticket: List[int], nearby_tickets: List[List[int]]) -> int:
    # Put all of the constraints together into one big valid-values pile
    all_valid_values = frozenset.union(*(x.valid_values for x in constraints))
    # Filter the nearby list down to just valid tickets
    valid_nearby_tickets = [x for x in nearby_tickets if is_valid_ticket(all_valid_values, x)]
    # Figure out which indices go with which field names
    field_indices = map_fields(constraints, valid_nearby_tickets)
    # Filter the values on your ticket down to just the ones whose name starts with "departure"
    your_departure_values = [x for i, x in enumerate(your_ticket) if field_indices[i].startswith("departure")]
    # Reduce it down to a single number for answer purposes
    return prod(your_departure_values)


def main():
    constraint_list, yours, nearby = ingest_input(read_data())
    print(f"Part one: {part_one(constraint_list, nearby)}")
    print(f"Part two: {part_two(constraint_list, yours, nearby)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

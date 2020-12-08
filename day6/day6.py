from functools import reduce
import string
from collections import Counter

test = """abc

a
b
c

ab
ac

a
a
a
a

b"""

test = open("/home/emathey/git-repos/input.txt").read()
groups = test.split("\n\n")

letter_filter = lambda answer: answer in string.ascii_letters

group_answers = [
    set(filter(letter_filter, person)) for person in groups  # Stripping white space
]

# Sum of the set lengths
part1 = reduce(lambda total, answer: total + len(answer), group_answers, 0)

# Count the number of people who said yes to each individual question
answer_counters = [Counter(filter(letter_filter, person)) for person in groups]

# Count how many individual people are part of each group
group_sizes = [len(person.split("\n")) for person in groups]

part2 = 0
for counter, group_size in zip(answer_counters, group_sizes):
    # Count the number of answers that had the same number of responses as people in the group
    for count in counter.values():
        if count == group_size:
            part2 += 1

print(f"Part 1: {part1} Part 2: {part2}")

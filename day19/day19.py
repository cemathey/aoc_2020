import sys
from pprint import pprint
from typing import NamedTuple, Tuple


class Rule(NamedTuple):
    rule_id: str
    sub_rules: Tuple[str, ...]
    base_rule: bool
    char: str


def parse_rules(raw_rules):
    # Every rule is either a combination of other rules, or a character to match against

    rule_tree = {}

    for raw_rule in raw_rules.splitlines():
        rule_id, child_rules = raw_rule.split(": ")
        # rule_id = int(rule_id)
        # Base rule!
        if '"' in child_rules:
            char = child_rules[1]
            rule = Rule(rule_id, tuple(), True, char)
            rule_tree[rule_id] = rule
        else:
            sub_rules = tuple(char for char in child_rules.split())
            rule = Rule(rule_id, sub_rules, False, "")
            rule_tree[rule_id] = rule

        # print(f"{left=} {right=}")

    return rule_tree


def decipher_rules(rules_tree):
    rule = rules_tree[0]

    for sub_rule in rule.sub_rules:
        print(sub_rule)


def split_sub_rules(sub_rules):
    left = right = None

    if "|" in sub_rules:
        pipe_idx = sub_rules.index("|")
        left = sub_rules[0:pipe_idx]
        right = sub_rules[pipe_idx + 1 :]
    else:
        left = sub_rules

    return left, right


if __name__ == "__main__":
    filename = sys.argv[1]

    contents = open(filename).read()
    rules, text = contents.split("\n\n")
    rules_tree = parse_rules(rules)

    top_rule = rules_tree["0"]

    combinations = []
    combo = []

    for rule in top_rule.sub_rules:
        sub_rule = rules_tree[rule]

        if sub_rule.base_rule:
            combo.append(rule)
        else:
            left, right = split_sub_rules(sub_rule.sub_rules)

            if left:
                combinations.append(combo + list(left))

            if right:
                combinations.append(combo + list(right))


# 0: 1 2
# 1: "a"
# 2: 1 3 | 3 1
# 3: "b"

# a a b
# a b a
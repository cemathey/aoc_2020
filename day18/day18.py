import sys
import string
from collections import defaultdict, deque

OPERATORS = ("+", "-", "*")


def tokenize(raw_expression):
    """Split the given string expression into discrete tokens ignoring whitespace."""
    token = []

    discrete_tokens = ("(", ")", "+", "-", "*")

    for char in raw_expression:
        if char in discrete_tokens:
            if token:
                yield "".join(token)
                token = []
            yield char
        elif char in string.digits:
            token.append(char)

    if token:
        yield "".join(token)


def build_expression_tree(tokens):
    expressions = defaultdict(list)
    # expressions = []
    sub_expr = []
    depth = 0
    for idx, token in enumerate(tokens):
        if token == "(":
            if sub_expr:
                expressions[depth].append(sub_expr)
                # expressions.append(sub_expr)
            sub_expr = []
            depth += 1
        elif token == ")":
            if sub_expr:
                expressions[depth].append(sub_expr)
                # expressions.append(sub_expr)
            sub_expr = []
            depth -= 1
        else:
            sub_expr.append(token)

    return expressions


def build_expression_tree(tokens):

    evaluatable = ""
    open_indexes = []

    valid = False
    while not valid:

        total = eval(evaluatable)

        if total:
            valid = True

        for idx, token in enumerate(tokens):
            if token == "(":
                open_indexes.append(idx)
            elif token == ")":
                pass
            else:
                pass


if __name__ == "__main__":
    filename = sys.argv[1]

    raw_expressions = [line.strip() for line in open(filename).readlines()]

    tokens = list(tokenize(raw_expressions[0]))

    tree = build_expression_tree(tokens)

    pass
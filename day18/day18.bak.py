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


def perform_operation(left, operator, right):
    """Calculate the value of the given operands and operator."""
    total = 0
    if operator == "+":
        total = left + right
    elif operator == "-":
        total = left - right
    elif operator == "*":
        total = left * right

    return total


def parse_expression_tree(tokens):
    """Build a tree of expressions from the given tokens at each depth in the expression."""

    expression_tree = defaultdict(deque)

    depth = 1

    sub_expression = deque()
    for idx, token in enumerate(tokens):
        if token == "(":
            if sub_expression:
                expression_tree[depth].append(deque(sub_expression))
                sub_expression = deque()
            depth += 1
        elif token == ")":
            expression_tree[depth].append(deque(sub_expression))
            sub_expression = deque()
            depth -= 1
        else:
            sub_expression.append(token)
    else:
        expression_tree[depth].append(tuple(sub_expression))

    return expression_tree


def eval_simple_expression(expression):
    operands = deque()
    operators = deque()

    total = 0
    for token in expression:
        if token in OPERATORS:
            operators.append(token)
        else:
            operands.append(int(token))

    while operators:
        left = operands.popleft()
        right = operands.popleft()
        operator = operators.popleft()

        sub_total = perform_operation(left, operator, right)
        operands.appendleft(sub_total)
        total = sub_total

    return total


def solve(expression):
    tokens = tuple(tokenize(expression))
    expression_tree = parse_expression_tree(tokens)
    expression_as_str = "".join(tokens)
    while len(expression_tree) > 1:
        highest = max(expression_tree.keys())

        expression_as_str = "".join(tokens)
        for sub_expression in expression_tree[highest]:
            padded_sub_expression = sub_expression.copy()
            padded_sub_expression.appendleft("(")
            padded_sub_expression.append(")")
            sub_expression_as_str = "".join(padded_sub_expression)
            start = expression_as_str.find(sub_expression_as_str)
            stop = len(sub_expression_as_str) + start
            val = eval_simple_expression(sub_expression)
            expression_as_str = (
                expression_as_str[0:start] + str(val) + expression_as_str[stop:]
            )

        tokens = tuple(tokenize(expression_as_str))
        expression_tree = parse_expression_tree(tokens)
    else:
        _ = tuple(tokenize(expression_as_str))
        return eval_simple_expression(_)


if __name__ == "__main__":
    filename = sys.argv[1]

    raw_expressions = [line.strip() for line in open(filename).readlines()]

    total = 0
    for expression in raw_expressions:
        print(expression)
        total += solve(expression)

    print(f"Part 1: {total=}")

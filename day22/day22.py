import sys
from collections import deque
from typing import Deque, Tuple, NamedTuple
from copy import copy, deepcopy
from pprint import pprint


class Deck(NamedTuple):
    cards: Deque[int]
    winning: bool


def build_decks(filename):
    """Build each players decks from the given file."""
    first_deck, second_deck = open(filename).read().split("\n\n")

    # Grab each card value skipping the deck name
    player1_deck: Deque[int] = deque(int(card) for card in first_deck.splitlines()[1:])
    player2_deck: Deque[int] = deque(int(card) for card in second_deck.splitlines()[1:])

    return Deck(player1_deck, False), Deck(player2_deck, False)


def play_game(player1_deck: Deck, player2_deck: Deck) -> int:
    """Play the game until one deck is empty and return both decks."""

    # Play until one deck is empty
    while player1_deck.cards and player2_deck.cards:
        # Top of the deck is the left side of the deque
        player1_card = player1_deck.cards.popleft()
        player2_card = player2_deck.cards.popleft()

        # Ties aren't possible?
        if player1_card > player2_card:
            player1_deck.cards.append(player1_card)
            player1_deck.cards.append(player2_card)
        else:
            player2_deck.cards.append(player2_card)
            player2_deck.cards.append(player1_card)

    return score_decks(player1_deck, player2_deck)


def decks_in_history(history, deck1, deck2):
    return tuple(deck1) in history or tuple(deck2) in history


def copy_n_cards(deck: Deck, num_cards):
    return Deck(deck.cards[:num_cards], deck.winning)


def recursive_game(player1_deck: Deck, player2_deck: Deck, history=set()):

    if decks_in_history(history, player1_deck.cards, player2_deck.cards):
        # player 1 wins
        return Deck(player1_deck.cards, True), Deck(player2_deck.cards, False)

    history.add(tuple(player1_deck.cards))
    history.add(tuple(player2_deck.cards))

    player1_card = player1_deck.cards.popleft()
    player2_card = player2_deck.cards.popleft()

    if (
        len(player1_deck.cards) >= player1_card
        and len(player2_deck.cards) >= player1_card
    ):
        # Recurse
        player1_deck_copy = copy_n_cards(player1_deck, player1_card)
        player2_deck_copy = copy_n_cards(player2_deck, player2_card)
        return recursive_game(player1_deck_copy, player2_deck_copy, history)
    elif player1_card > player2_card:
        # player 1 wins
        player1_deck.cards.append(player1_card)
        player1_deck.cards.append(player2_card)
        return Deck(player1_deck.cards, True), Deck(player2_deck.cards, False)
    else:
        # player 2 wins
        player2_deck.cards.append(player2_card)
        player2_deck.cards.append(player1_card)
        return Deck(player1_deck.cards, False), Deck(player2_deck.cards, True)


def score_decks(player1_deck: Deck, player2_deck: Deck) -> int:
    """Score the given decks."""
    if player1_deck.cards:
        winning_deck = player1_deck.cards
    else:
        winning_deck = player2_deck.cards

    positions = tuple(pos for pos in range(len(winning_deck), 0, -1))
    return sum(position * card for position, card in zip(positions, winning_deck))


if __name__ == "__main__":
    filename = sys.argv[1]

    player1, player2 = build_decks(filename)
    score: int = play_game(player1, player2)

    print(f"Part 1 winning score= {score}")

    player1, player2 = build_decks(filename)
    player1, player2 = recursive_game(player1, player2)
    pprint(player1)
    pprint(player2)
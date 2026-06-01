"""
models.py

Core card/deck data structures for Texas Hold'em.
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional

#create rank and suit mappings
#rank dict for str to int
RANK_MAP: Dict[str, int] = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}
#rank dict for int to str
RANK_INV: Dict[int, str] = {v: k for k, v in RANK_MAP.items()}
#suit list
SUIT_MAP: List[str] = ["h", "d", "s", "c"]  # hearts, diamonds, spades, clubs


class Card:
    '''
    Docstring for Card
    Create card class
    Every card has a rank and a suit,and can be compared to other cards
    Attributes:
        rank (int): The rank of the card (2-14) #see RANK_MAP for mapping
        suit (str): The suit of the card ('h', 'd', 's', 'c') 
    Methods:
        __str__: Returns string representation of the card
        __repr__: Returns string representation of the card
        __eq__: Compares two cards for equality
        __hash__: Returns hash of the card(in order to successfully conduct __eq__)
        from_string: Creates a Card object from a string representation(etc 'Ah' for Ace of hearts)
    '''
    def __init__(self, rank: int, suit: str):
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return f"{RANK_INV[self.rank]}{self.suit}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self) -> int:
        return hash((self.rank, self.suit))

    @staticmethod
    def from_string(card_str: str) -> "Card":
        if len(card_str) != 2:#denfensive programming
            raise ValueError(f"Invalid card string: {card_str!r}")
        rank_char = card_str[0].upper()
        suit_char = card_str[1].lower()
        if rank_char not in RANK_MAP:
            raise ValueError(f"Invalid rank: {rank_char!r}")
        if suit_char not in SUIT_MAP:
            raise ValueError(f"Invalid suit: {suit_char!r}")
        return Card(RANK_MAP[rank_char], suit_char)


class Deck:
    '''
    Docstring for Deck
    create deck class
    A deck contains a list of Card objects,and can be shuffled and dealt from
    Attributes:
        cards (List[Card]): we use 'for' to iterate through all cards to consist into a full deck of 52 cards
        excluded_cards (Optional[List[Card]]): use this parameter to exclude specific cards from the deck
    Methods:
        shuffle: Shuffles the deck using an optional random number generator
        deal: Deals a specified number of cards from the deck, removing them from the deck

    '''
    def __init__(self, excluded_cards: Optional[List[Card]] = None):
        exclusions = set(excluded_cards or [])
        self.cards: List[Card] = [
            Card(rank, suit)
            for rank in range(2, 15)
            for suit in SUIT_MAP
            if Card(rank, suit) not in exclusions
        ]

    def shuffle(self, rng: Optional[random.Random] = None) -> None:
        if rng is None:
            random.shuffle(self.cards)
        else:
            rng.shuffle(self.cards)

    def deal(self, n: int) -> List[Card]:
        if n > len(self.cards):
            raise ValueError("Not enough cards in deck.")
        dealt = self.cards[-n:]
        self.cards = self.cards[:-n]
        return dealt


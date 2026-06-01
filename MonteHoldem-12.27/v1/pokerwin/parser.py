"""
parser.py

Input parsing and validation helpers.
"""

from __future__ import annotations

from typing import List

from .models import Card


def _split_cards(s: str) -> List[str]:
    ''' helper function to split input string into card parts '''
    s = (s or "").strip() # trim whitespace
    if not s:
        return []
    parts = s.split() # try splitting by space (e.g. 'Ah Kd')
    if len(parts) > 1:
        return parts

    # if no spaces, handle compact format (e.g. 'AhKd')
    compact = parts[0]
    if len(compact) % 2 != 0: # check if string length is valid
        raise ValueError(f"Invalid card string: {s!r}")
    return [compact[i : i + 2] for i in range(0, len(compact), 2)] # split into 2-char chunks


def parse_cards(s: str) -> List[Card]:
    ''' convert string parts into Card objects '''
    return [Card.from_string(p) for p in _split_cards(s)]


def parse_hand(hand_str: str) -> List[Card]:
    ''' parse and validate hero's 2-card hand '''
    cards = parse_cards(hand_str)
    if len(cards) != 2: # check hand length
        raise ValueError("Hand must be exactly 2 cards (e.g. 'Ah Kd').")
    if len(set(cards)) != 2: # check duplicate cards
        raise ValueError("Hand contains duplicate cards.")
    return cards


def parse_board(board_str: str) -> List[Card]:
    ''' [!] parse and validate community cards (0-5 cards) '''
    cards = parse_cards(board_str)
    if not (0 <= len(cards) <= 5): # check board length range
        raise ValueError("Board must contain 0..5 cards (e.g. 'Th Jh Qh').")
    if len(set(cards)) != len(cards): # check duplicate cards in board
        raise ValueError("Board contains duplicate cards.")
    return cards


def validate_no_overlap(hand: List[Card], board: List[Card]) -> None:
    ''' [!] ensure hero hand and board do not share the same cards '''
    overlap = set(hand) & set(board) # find intersection
    if overlap: # if overlap exists, raise error
        raise ValueError(f"Hand and board overlap: {sorted(map(str, overlap))}")
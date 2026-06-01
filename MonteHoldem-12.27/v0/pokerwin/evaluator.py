"""
evaluator.py

Evaluates a 7-card Texas Hold'em hand into a comparable tuple score.
"""

from __future__ import annotations

from collections import Counter
from typing import List, Optional, Tuple

from .models import Card

# Hand rank scores
HIGH_CARD = 0
ONE_PAIR = 1
TWO_PAIR = 2
THREE_OF_A_KIND = 3
STRAIGHT = 4
FLUSH = 5
FULL_HOUSE = 6
FOUR_OF_A_KIND = 7
STRAIGHT_FLUSH = 8


class HandEvaluator:
    '''
    Docstring for HandEvaluator
    Evaluates a 7-card Texas Hold'em hand into a comparable tuple score.
    with higher tuple values indicating stronger hands.
    for the first element of the tuple indicates the hand rank, it scores from 0 to 8 (see above)
    the rest of the tuple contains tiebreaker information based on the hand type (it varies by hand type).
    we use the 'Counter' to count occurrences of each rank in the hand,
    then can know how to determine the hand types which is related to the counts.
    Methods:
        evaluate: Evaluates a list of 7 Card objects and returns a tuple score
            we check from highest rank to lowest rank one by one to determine the hand type,
            if a hand type is confirmed, we return the corresponding score tuple immediately.
        get_flush: Helper method to check for flushes
        get_straight_high_card: Helper method to check for straights
    '''
    @staticmethod
    def evaluate(cards: List[Card]) -> Tuple[int, ...]:
        if len(cards) != 7: #defensive programming
            raise ValueError(f"HandEvaluator.evaluate() requires exactly 7 cards, got {len(cards)}")

        cards_sorted = sorted(cards, key=lambda c: c.rank, reverse=True) #sort cards by rank descending

        # Check for straight flush
        flush_suit, flush_cards = HandEvaluator._get_flush(cards_sorted)
        flush_score: Optional[Tuple[int, ...]] = None
        if flush_suit:
            sf_rank = HandEvaluator._get_straight_high_card(flush_cards)
            if sf_rank:
                return (STRAIGHT_FLUSH, sf_rank)
            flush_score = (FLUSH, *[c.rank for c in flush_cards[:5]])

        # Count occurrences of each rank
        ranks = [c.rank for c in cards_sorted]
        counts = Counter(ranks)
        sorted_counts = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
        count_values = [item[1] for item in sorted_counts]
        # Check for four of a kind
        if count_values[0] == 4:
            quad_rank = sorted_counts[0][0]
            kicker = max(r for r in ranks if r != quad_rank)
            return (FOUR_OF_A_KIND, quad_rank, kicker)
        # Check for full house
        if count_values[0] == 3 and count_values[1] >= 2:
            trip_rank = sorted_counts[0][0]
            pair_rank = sorted_counts[1][0]
            return (FULL_HOUSE, trip_rank, pair_rank)
        # Check for flush, the flush is already computed in straight flush check
        if flush_score is not None:
            return flush_score
        # Check for straight
        st_rank = HandEvaluator._get_straight_high_card(cards_sorted)
        if st_rank:
            return (STRAIGHT, st_rank)
        # Check for three of a kind
        if count_values[0] == 3:
            trip_rank = sorted_counts[0][0]
            kickers = [x[0] for x in sorted_counts[1:]][:2]
            return (THREE_OF_A_KIND, trip_rank, *kickers)
        # Check for two pair
        if count_values[0] == 2 and count_values[1] == 2:
            pair1 = sorted_counts[0][0]
            pair2 = sorted_counts[1][0]
            kicker = max(r for r in ranks if r not in (pair1, pair2))
            return (TWO_PAIR, pair1, pair2, kicker)
        # Check for one pair
        if count_values[0] == 2:
            pair_rank = sorted_counts[0][0]
            kickers = [x[0] for x in sorted_counts[1:]][:3]
            return (ONE_PAIR, pair_rank, *kickers)
        # High card
        return (HIGH_CARD, *ranks[:5])

    @staticmethod
    def _get_flush(cards: List[Card]) -> Tuple[str, List[Card]]:
        suits = [c.suit for c in cards]
        suit_counts = Counter(suits)
        for suit, count in suit_counts.items():
            if count >= 5:
                flush_cards = [c for c in cards if c.suit == suit]
                return suit, flush_cards #return suit and flush cards
        return "", []# No flush found,return empty string and empty list

    @staticmethod
    def _get_straight_high_card(cards: List[Card]) -> int:
        unique_ranks = sorted({c.rank for c in cards}, reverse=True)#{use set to get unique ranks}
        if len(unique_ranks) < 5:
            return 0

        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - 4 == unique_ranks[i + 4]:
                return unique_ranks[i]
        # Check for wheel straight (A-2-3-4-5),special case
        if 14 in unique_ranks and all(r in unique_ranks for r in (5, 4, 3, 2)):
            return 5

        return 0


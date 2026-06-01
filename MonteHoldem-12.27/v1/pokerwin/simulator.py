"""
simulator.py

Monte Carlo equity simulation logic (ties are split as pot equity).
"""

from __future__ import annotations

import random
from typing import List, Optional

from .evaluator import HandEvaluator
from .models import Card, Deck


class MonteCarloSimulator:
    '''
    Docstring for MonteCarloSimulator
    Simulates poker hands to calculate equity percentage for a given hero hand.
    Attributes:
        hero_hand (List[Card]): The hero's 2-card hand
        players (int): Total number of players at the table (including hero)
        sims (int): Number of Monte Carlo simulations to run
        seed (Optional[int]): Optional random seed for reproducibility
        [!]board (Optional[List[Card]]): Known community cards (0 to 5 cards)
        [!]opponent_range (Optional[str]): Opponent hand range model ('tight', 'standard', 'loose', 'random')
        [!]active_opponents (Optional[int]): Number of active opponents (default: players - 1)
        [!]opponent_ranges (Optional[List[str]]): Specific range models for each opponent seat
    Methods:
        _validate: Validates the input parameters,pretending user input worng inputs
        run: Runs the Monte Carlo simulation and returns the equity percentage
    '''
    def __init__(
        self,
        *,
        hero_hand: List[Card],
        board: Optional[List[Card]] = None,#[!]cards in board must be 3~5
        players: int,
        sims: int,
        seed: Optional[int] = None,
        opponent_range: Optional[str] = None,#[!]
        active_opponents: Optional[int] = None,#[!]players not discarded
        opponent_ranges: Optional[List[str]] = None,#[!]
    ) -> None:
        self.hero_hand = list(hero_hand)
        self.board = list(board or [])
        self.players = players
        self.sims = sims
        self.seed = seed
        self.opponent_range = (opponent_range or "random").lower()
        self.active_opponents = active_opponents
        self.opponent_ranges = [str(x).lower() for x in (opponent_ranges or [])]
        self._rng = random.Random(seed)
        self._validate()

    def _validate(self) -> None:#check user input validity
        if len(self.hero_hand) != 2:
            raise ValueError("Hand must contain exactly 2 cards.")
        if len(set(self.hero_hand)) != 2:
            raise ValueError("Hand contains duplicate cards.")
        if not (3 <= len(self.board) <= 5):#[!] check board length
            raise ValueError("Board must contain 3~5 cards.")
        if len(set(self.board)) != len(self.board): #[!] check duplicate cards in board
            raise ValueError("Board contains duplicate cards.")
        overlap = set(self.hero_hand) & set(self.board)
        if overlap:#[!] check overlap between hand and board
            raise ValueError(f"Hand and board overlap: {sorted(map(str, overlap))}")
        if self.players < 2:
            raise ValueError("players must be >= 2 (total players including hero).")
        if self.active_opponents is not None:
            if not (0 <= self.active_opponents <= self.players - 1):
                raise ValueError("active_opponents must be between 0 and players-1")
        if self.opponent_ranges:
            opponents_n = self.active_opponents if self.active_opponents is not None else (self.players - 1)
            if len(self.opponent_ranges) != opponents_n:
                raise ValueError("opponent_ranges length must equal number of active opponents")
        if self.sims <= 0:
            raise ValueError("sims must be > 0.")

        remaining_cards = 52 - (len(self.hero_hand) + len(self.board))
        opponents_n = self.active_opponents if self.active_opponents is not None else (self.players - 1)
        needed_cards = (5 - len(self.board)) + (opponents_n * 2)
        if remaining_cards < needed_cards:
            raise ValueError("Not enough cards remaining to deal.")

    def run(self) -> float:
        total_share = 0.0

        opponents_n = self.active_opponents if self.active_opponents is not None else (self.players - 1)

        # Determine the range constraint for each opponent seat.
        ranges_for_opponents: List[str]
        if self.opponent_ranges:
            ranges_for_opponents = self.opponent_ranges
        else:
            ranges_for_opponents = [self.opponent_range for _ in range(opponents_n)]

        for _ in range(self.sims):
            excluded = self.hero_hand + self.board
            deck = Deck(excluded_cards=excluded)
            deck.shuffle(self._rng)

            missing = 5 - len(self.board) #[!] number of cards needed to complete the board
            board = self.board + (deck.deal(missing) if missing else []) #[!] complete the board to 5 cards
            opponents: List[List[Card]] = []
            for range_name in ranges_for_opponents:
                hand = _deal_hand_in_range(deck, self._rng, range_name)
                opponents.append(hand)

            hero_score = HandEvaluator.evaluate(self.hero_hand + board)
            all_scores = [hero_score] + [HandEvaluator.evaluate(h + board) for h in opponents]
            best = max(all_scores)
            if hero_score == best:
                total_share += 1.0 / all_scores.count(best)

        return (total_share / self.sims) * 100.0


def calculate_equity_percent(
    hero_hand: List[Card],
    *,
    board: Optional[List[Card]] = None,
    players: int,
    sims: int,
    seed: Optional[int] = None,
    opponent_range: Optional[str] = None,
    active_opponents: Optional[int] = None,
    opponent_ranges: Optional[List[str]] = None,
) -> float:
    return MonteCarloSimulator(
        hero_hand=hero_hand,
        board=board,
        players=players,
        sims=sims,
        seed=seed,
        opponent_range=opponent_range,
        active_opponents=active_opponents,
        opponent_ranges=opponent_ranges,
    ).run()

#------------------------------------------------------------
#[!]all code below is newly added for opponent range modeling
def _hand_in_range(hand: List[Card], range_name: str) -> bool:
    """[!]Very lightweight opponent range model.
    range_name: one of ['tight', 'standard', 'loose']
    the range means which hands are acceptable to deal to represent that opponent type.
    the tight hand only accepts very strong hands, loose accepts many hands, standard is in between.
    tight: pairs TT+, AK, AQ, AJs+, KQs
    standard: pairs 77+, suited aces A2s+, broadways, suited connectors
    loose: pairs any, many suited connectors, suited aces, offsuit broadways KJo+, ATo+
    random: all hands accepted    
    """
    if len(hand) != 2:
        return False
    c1, c2 = hand[0], hand[1]
    r1, r2 = c1.rank, c2.rank
    s1, s2 = c1.suit, c2.suit
    high = lambda r: r >= 10  # T, J, Q, K, A
    is_pair = r1 == r2
    is_suited = s1 == s2
    hi = max(r1, r2)
    lo = min(r1, r2)
    gap = abs(r1 - r2)

    # Helper predicates
    is_connector = gap == 1
    is_one_gap = gap == 2

    # AA..22
    if range_name == "tight":
        # Pairs TT+, AK, AQ, AJs+, KQs
        if is_pair and hi >= 10:
            return True
        if hi == 14 and lo == 13:  # AK
            return True
        if hi == 14 and lo == 12:  # AQ
            return True
        if is_suited and ((hi == 14 and lo >= 11) or (hi == 13 and lo == 12)):  # AJs+, KQs
            return True
        return False

    if range_name == "standard":
        # Pairs 77+, suited aces A2s+, broadways, suited connectors T9s+; offsuit AJo+, KQo
        if is_pair and hi >= 7:
            return True
        if is_suited and hi == 14:  # Axs
            return True
        if high(r1) and high(r2):  # both broadways
            if is_suited:
                return True
            # Offsuit AJo+, KQo
            if (hi == 14 and lo >= 11) or (set([r1, r2]) == set([13, 12])):
                return True
        if is_suited and ((is_connector and hi >= 10) or (is_one_gap and hi >= 11)):
            return True
        return False

    if range_name == "loose":
        # Pairs any, many suited connectors, suited aces, offsuit broadways KJo+, ATo+
        if is_pair:
            return True
        if is_suited and (hi == 14 or is_connector or is_one_gap or lo >= 5):
            return True
        if (hi == 14 and lo >= 10):  # ATo+
            return True
        if high(r1) and high(r2) and lo >= 11:  # KJo+
            return True
        return False

    # default random: always accept
    return True


def _deal_hand_in_range(deck: Deck, rng: random.Random, range_name: str) -> List[Card]:
    """[!]Deal exactly two cards from the given deck that satisfy range_name.
    Uses rejection sampling but keeps dealing from the same shared deck.
    To avoid rare infinite loops with narrow ranges late in the deck,
    we allow a bounded number of attempts and then fall back to random.
    """
    range_name = (range_name or "random").lower()
    if range_name == "random":
        return deck.deal(2)

    attempts = 0
    max_attempts = 200
    while attempts < max_attempts:
        if len(deck.cards) < 2:
            break
        hand = deck.deal(2)
        if _hand_in_range(hand, range_name):
            return hand
        # Put back and reshuffle remaining deck to keep sampling unbiased-ish.
        deck.cards.extend(hand)
        deck.shuffle(rng)
        attempts += 1

    # Fallback: if we couldn't satisfy the range, just deal random.
    return deck.deal(2)

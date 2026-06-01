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
    Methods:
        _validate: Validates the input parameters,pretending user input worng inputs
        run: Runs the Monte Carlo simulation and returns the equity percentage
    '''
    def __init__(
        self,
        *,
        hero_hand: List[Card],
        players: int,
        sims: int,
        seed: Optional[int] = None,
    ) -> None:
        self.hero_hand = list(hero_hand)
        self.players = players
        self.sims = sims
        self.seed = seed
        self._rng = random.Random(seed)
        self._validate()

    def _validate(self) -> None:
        if len(self.hero_hand) != 2:#check hero hand length
            raise ValueError("Hand must contain exactly 2 cards.")
        if len(set(self.hero_hand)) != 2:#check duplicate cards
            raise ValueError("Hand contains duplicate cards.")
        if self.players < 2:#check players number
            raise ValueError("players must be >= 2 (total players including hero).")
        if self.sims <= 0:#check sims number
            raise ValueError("sims must be > 0.")

        remaining_cards = 52 - len(self.hero_hand)#calculate remaining cards in deck
        needed_cards = 5 + ((self.players - 1) * 2)#5 board cards + 2 cards per opponent
        if remaining_cards < needed_cards:#check if enough cards remain
            raise ValueError("Not enough cards remaining to deal.")

    def run(self) -> float:
        total_share = 0.0

        for _ in range(self.sims):#use Monte Carlo method to simulate hands
            deck = Deck(excluded_cards=self.hero_hand)#instantiate deck excluding your hand
            deck.shuffle(self._rng)

            board = deck.deal(5)#deal 5 community cards
            opponents = [deck.deal(2) for _ in range(self.players - 1)]#deal 2 cards for each opponent

            hero_score = HandEvaluator.evaluate(self.hero_hand + board)#your hand + board score
            all_scores = [hero_score] + [HandEvaluator.evaluate(h + board) for h in opponents]#your score + opponents' scores
            best = max(all_scores)#determine best score
            if hero_score == best:#if you win, plus 1 count ,except ties
                total_share += 1.0 / all_scores.count(best)# split pot if tie

        return (total_share / self.sims) * 100.0

'''
function to instance the MonteCarloSimulator and return equity percentage
'''
def calculate_equity_percent(
    hero_hand: List[Card], *, players: int, sims: int, seed: Optional[int] = None
) -> float:
    return MonteCarloSimulator(hero_hand=hero_hand, players=players, sims=sims, seed=seed).run()


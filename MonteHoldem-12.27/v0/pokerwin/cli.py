"""
cli.py

CLI entrypoint for v0.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .models import Card
from .simulator import calculate_equity_percent

#turn a string of cards into a list of Card objects
#because user input is a string, but function need list[Card] objects
def _parse_cards(cards_str: str) -> List[Card]:
    s = cards_str.strip()
    if not s:
        return []
    parts = s.split()
    if len(parts) == 1:
        compact = parts[0]
        if len(compact) % 2 != 0:
            raise ValueError(f"Invalid card string: {cards_str!r}")
        parts = [compact[i : i + 2] for i in range(0, len(compact), 2)]
    return [Card.from_string(p) for p in parts]

#defensive check for hand input
def _parse_hand(hand_str: str) -> List[Card]:
    cards = _parse_cards(hand_str)
    if len(cards) != 2:
        raise ValueError("Hand must be exactly 2 cards (e.g. 'Ah Kd').")
    if len(set(cards)) != 2:
        raise ValueError("Hand contains duplicate cards.")
    return cards

'''
function to parse CLI arguments,
input hand, players number, sims number and seed number into terminal,
hand and players are required arguments,
sims and seed are optional arguments with default values
example:
    python -m pokerwin.cli --hand "Ah Kd" --players 6 --sims 20000 --seed 36;
    python -m pokerwin.cli --hand "As Ad" --players 2
'''
def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Texas Hold'em equity simulator (v0)")
    parser.add_argument("--hand", required=True, help="Hole cards, e.g. 'Ah Kd'")
    parser.add_argument("--players", type=int, required=True, help="Total players including hero (>=2)")
    parser.add_argument("--sims", type=int, default=10000, help="Simulations (default: 10000)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed (optional)")
    args = parser.parse_args(argv)

    hero_hand = _parse_hand(args.hand)
    equity = calculate_equity_percent(hero_hand, players=args.players, sims=args.sims, seed=args.seed)
    print(f"Equity: {equity:.2f}%")
    return 0


#run the MonteCarloSimulator from command line
if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        raise SystemExit(2)


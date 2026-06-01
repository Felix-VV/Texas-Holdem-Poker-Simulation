"""
cli.py

CLI entrypoint for v2.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from typing import List, Optional

from .parser import parse_board, parse_hand, validate_no_overlap
from .simulator import calculate_equity_percent


def main(argv: Optional[List[str]] = None) -> int:# CLI main function
    parser = argparse.ArgumentParser(description="Texas Hold'em equity simulator (v2)")
    parser.add_argument("--hand", required=True, help="Hole cards, e.g. 'Ah Kd'")
    parser.add_argument("--board", default="", help="Known board cards (0..5), e.g. 'Th Jh Qh'")
    parser.add_argument("--players", type=int, default=6, help="Total players including hero (must be 6 for 6-max)")
    parser.add_argument("--sims", type=int, default=10_000, help="Simulations (default: 10000)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed (optional)")
    parser.add_argument(
        "--opponent-range",
        default="standard",
        help="Default opponent range: random/tight/standard/loose (default: standard)",
    )
    parser.add_argument("--active-opponents", type=int, default=None, help="Number of active opponents (default: players-1)")
    parser.add_argument("--opponent-ranges", nargs="*", default=None, help="Individual ranges for each opponent, e.g. 'tight loose standard'")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    logger = logging.getLogger("pokerwin")

    hero_hand = parse_hand(args.hand)
    board = parse_board(args.board)
    validate_no_overlap(hero_hand, board)

    if args.players != 6:
        raise ValueError("This tool supports 6-max only: players must be 6.")

    logger.info(
        "config hand=%s board=%s players=%s sims=%s seed=%s opponent_range=%s active_opponents=%s opponent_ranges=%s",
        " ".join(map(str, hero_hand)),
        " ".join(map(str, board)) if board else "[]",
        args.players,
        args.sims,
        args.seed,
        args.opponent_range,
        args.active_opponents,
        args.opponent_ranges,
    )

    start = time.perf_counter()
    equity = calculate_equity_percent(
        hero_hand,
        board=board,
        players=args.players,
        sims=args.sims,
        seed=args.seed,
        opponent_range=args.opponent_range,
        active_opponents=args.active_opponents,
        opponent_ranges=args.opponent_ranges,
    )
    elapsed = time.perf_counter() - start
    logger.info("done seconds=%.4f equity=%.4f", elapsed, equity)

    print(f"Equity: {equity:.2f}%")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        raise SystemExit(2)

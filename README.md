# Texas Hold'em Monte Carlo Equity Simulator

A from-scratch Texas Hold'em (6-max) equity calculator written in pure Python.
Given a hero's hole cards and any board state, it estimates win probability against
opponents via Monte Carlo simulation, with a hand-written 7-card evaluator at its core.

No poker libraries are used — the deck model, hand-ranking logic, and simulation engine
are all implemented from the ground up.

## What this project demonstrates

- **Non-trivial algorithm, written from scratch**: a 7-card hand evaluator that maps any
  hand to a comparable tuple score, correctly handling straights, flushes, full houses,
  the wheel straight (A-2-3-4-5), and kicker tie-breaks.
- **Probabilistic modeling**: Monte Carlo estimation of equity with correct split-pot
  (tie) handling.
- **Clean OOP separation of concerns**: card/deck models, evaluator, parser, simulator,
  and interface layers are decoupled and independently testable.
- **Iterative engineering**: the same problem solved across three versions (CLI MVP →
  flexible utility → web app), showing how scope and quality grew over time.
- **Testing**: edge-case unit tests with `pytest`.

## Project structure

```
MonteHoldem-12.27/
├── v0/            # MVP: core models, evaluator, basic Monte Carlo via CLI
├── v1/            # Adds dynamic board input, opponent range modeling, input validation
└── v2/            # Adds pytest test suite + Flask web GUI
    ├── pokerwin/
    │   ├── models.py       # Card / Deck data structures
    │   ├── evaluator.py    # 7-card hand evaluator -> tuple score
    │   ├── parser.py       # Card-string parsing & validation
    │   ├── simulator.py    # Monte Carlo engine + opponent range models
    │   └── cli.py          # Command-line entry point
    ├── server.py           # Flask API exposing /calculate
    ├── index.html          # Web front-end (pick cards, view equity)
    └── tests/              # pytest unit tests
```

`v2/` is the most complete version. `v0/` and `v1/` are kept to show the development path.

## Quick start (CLI)

Run from the `v2/` directory:

```bash
cd v2

# Flop example: AKs on a Q-J-T two-tone board, 6 players
python -m pokerwin.cli --hand "Ah Kh" --board "Qh Jh Ts" --players 6 --sims 10000

# Pre-flop example: pocket aces against 5 opponents
python -m pokerwin.cli --hand "Ah As" --players 6 --sims 10000

# Reproducible run with a fixed seed
python -m pokerwin.cli --hand "Ah As" --board "2c 7d Th" --sims 20000 --seed 7
```

Board cards are optional and may be 0 (pre-flop), 3 (flop), 4 (turn), or 5 (river).
Output is the hero's estimated equity, e.g. `Equity: 86.27%`.

### Useful flags

| Flag | Description | Default |
|---|---|---|
| `--hand` | Hero's two hole cards, e.g. `"Ah Kd"` | required |
| `--board` | Known community cards (0/3/4/5) | `""` (pre-flop) |
| `--players` | Total players including hero (6-max) | `6` |
| `--sims` | Number of Monte Carlo iterations | `10000` |
| `--seed` | Random seed for reproducibility | none |
| `--opponent-range` | `random` / `tight` / `standard` / `loose` | `standard` |

## Web interface (v2)

```bash
cd v2
pip install flask flask-cors
python server.py
```

Then open `index.html` in a browser to pick cards visually and view the calculated equity.

## Running the tests

```bash
cd v2
pip install pytest
python -m pytest tests/ -q
```

## How it works

Card ranks are encoded as integers (2–14, where 14 = Ace) so hands can be compared
numerically. The evaluator checks hand categories from strongest to weakest and returns
the first match as a tuple — for example `(FULL_HOUSE, trip_rank, pair_rank)` — so that
Python's native tuple comparison resolves both category and tie-breakers in one step.
The simulator deals random cards to opponents and the remaining board, evaluates every
hand, and accumulates the hero's share of each pot (ties split equally) over thousands of
iterations.

Opponent hand selection supports simple range profiles (tight / standard / loose) via
rejection sampling, so opponents can be modeled as something other than fully random.

## Limitations

- Equity only — betting, pot odds, and EV/GTO analysis are out of scope.
- Pure-Python sampling; very large simulation counts are limited by single-threaded speed.
- Opponent range models are coarse approximations, not full pre-flop charts.

## Tech

Python 3.7+ · standard library (`collections`, `random`, `argparse`, `logging`) · Flask
(web layer) · pytest (tests).

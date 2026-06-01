# PokerWin v2

CLI Texas Hold'em equity simulator with optional known community cards, logging, and tests.
For V2, we mainly develop a frontend by using Build web-based GUI operation page with Flask (backend) + JavaScript (frontend).
1.server.py is created to handle web requests
2.index.html is created to provide user interface
3.tests/ folder is created to include unit tests for core functionalities
4.add logging to record simulation parameters and results in cli.py

## Run

```bash
cd v2
python -m pokerwin.cli --hand "Ah Kd" --players 2 --sims 5000
```

Add known community cards (0..5):

```bash
python -m pokerwin.cli --hand "Ah Kd" --board "Th Jh Qh" --players 6 --sims 20000
```

Optional: set a seed for reproducible results:

```bash
python -m pokerwin.cli --hand "Ah Kd" --players 6 --sims 20000 --seed 42
```

## Tests

```bash
cd v2
pytest -q
```

## Web (optional)

```bash
cd v2
python server.py
```

Then open `v2/index.html` in a browser.

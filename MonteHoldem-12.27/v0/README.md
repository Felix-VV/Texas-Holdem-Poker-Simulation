# PokerWin v0

Minimal CLI-only Texas Hold'em equity simulator (Monte Carlo).

## Run

```bash
cd v0
python -m pokerwin.cli --hand "Ah Kd" --players 2 --sims 5000
```

Optional: set a seed for reproducible results:

```bash
python -m pokerwin.cli --hand "Ah Kd" --players 6 --sims 20000 --seed 42
```

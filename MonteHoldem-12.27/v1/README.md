# PokerWin v1

CLI Texas Hold'em equity simulator with optional known community cards and logging.
In V0, we simulate the basic model
For V1, we develop more features to make it more close to real card games.
1.The number of cards in board can be 3,4,5
2.We have set strategic tendencies for each opponents to simulate the scenarios that they would fold
3.A new parser file has been created to handle invalid user input parameters

The evaluator.py and models.py remain unchanged
For the rest of files, any change will be marked with an '!' in the preceding comments
use ctrl+F to search for '!' and check all the changes

## Run

```bash
cd v1
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

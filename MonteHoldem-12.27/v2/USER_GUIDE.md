# PokerWin v2 - User Guide

## 📋 Introduction
PokerWin v2 is a Texas Hold'em equity calculator with:
- Web interface for 6-max positions and per-position opponent ranges
- Command-line tool for quick equity checks
- Monte Carlo simulation for win-rate estimation

------

## 🚦 Zero-to-Run Quickstart (Beginner Friendly)
1) Install Python 3.7+ from https://www.python.org/downloads/ (Windows: check "Add Python to PATH").
2) Open the project folder in a terminal (macOS: Finder → right-click folder → Open in Terminal; Windows: type `cmd` in the folder address bar and press Enter).
3) Run the start script:
	 - macOS: double-click `open_web.command`.
	 - Windows: double-click `start_web_windows.bat` (if it closes instantly, see Windows section below).

4) The script installs dependencies and starts the server. Your browser should open a local address like `http://127.0.0.1:15002` (the script prints the exact URL). If the port is busy, use the port suggested in the message.
5) In the page, select hole cards/community cards, tick positions still in the pot, set opponent ranges, then click "Calculate Equity".

If scripts fail, use manual commands (macOS: `python3`, Windows: `python` or `py -3`):
```bash
# Install dependencies
pip install -r requirements.txt

# Start server
python server.py

```

---

## 🖥️ macOS User Guide

### Prerequisites
- Python 3.7 or higher
- Terminal application

### First run on a brand-new Mac (one-click script notes)
- `open_web.command` will automatically create a local virtual environment at `v2/.venv/` and install packages from `requirements.txt`.
- If you copy this folder to another Mac, you can still double-click `open_web.command` and it should work (as long as `python3` exists on that Mac).
- If you want a clean reinstall, delete the `v2/.venv/` folder and run the script again.

### If macOS blocks the script (Gatekeeper)
- If double-click shows "cannot be opened because it is from an unidentified developer":
	1) Right-click (or Control-click) `open_web.command` → Open → Open anyway.
	2) Or allow it in System Settings → Privacy & Security.
- If double-click does nothing (common after downloading from WeChat/Browser), remove the quarantine attribute:
	- `xattr -d com.apple.quarantine open_web.command`
- If the script is not executable, run: `chmod +x open_web.command`.

### Using the start script (recommended)
- In the project folder, double-click `open_web.command`. It installs dependencies (into `v2/.venv/`) and starts a local server.
- The script prints the exact URL to open (default port may differ from manual `python3 server.py`).

### Step 1: Check Python
```bash
python3 --version
```
If not 3.x, install from python.org.

### Step 2: Go to project directory
```bash
cd /path/to/MonteHoldem/v2
```

### Step 3: Install dependencies (manual fallback)
```bash
pip3 install flask flask-cors
```

### Step 3.5: Manual start (if the script fails)
```bash
python3 server.py
```
When you see `PokerWin v2 server: http://127.0.0.1:15000`, open that address in your browser.

### Step 4: Web interface usage
- Visit the shown URL (default `http://127.0.0.1:15000`).
- Select your hand (2 cards) and community cards (0-5 cards).
- Check positions that remain in the pot.
- Set opponent ranges (Tight/Standard/Loose/Random).
- Click "Calculate Equity".

### Command-line tool (macOS)
```bash
# Basic
python3 -m pokerwin.cli --hand "Ah Kd" --players 3 --sims 10000

# With board
python3 -m pokerwin.cli --hand "Ah Kd" --board "Qh Jh Th" --players 4 --sims 10000

# Default opponent range
python3 -m pokerwin.cli --hand "Ah Kd" --players 3 --sims 10000 --opponent-range tight

# Per-opponent ranges
python3 -m pokerwin.cli --hand "Ah Kd" --players 4 --opponent-ranges tight loose standard
```

Parameters:
- `--hand` hero hole cards (required), e.g., "Ah Kd"
- `--board` community cards (optional), e.g., "Qh Jh Th"
- `--players` total players including hero (required; web app supports 6-max)
- `--sims` number of simulations (default 10000)
- `--opponent-range` default range (random/tight/standard/loose)
- `--opponent-ranges` per-opponent ranges
- `--active-opponents` active opponents (default players-1)
- `--seed` random seed (optional)

---

## 🪟 Windows User Guide

### Prerequisites
- Python 3.7 or higher
- Command Prompt (CMD) or PowerShell

### Common first-run issues
- Double-click `start_web_windows.bat` closes immediately: open CMD/PowerShell in the project folder and run `start_web_windows.bat` so the window stays open.
- `'python' is not recognized`: reinstall Python and check "Add Python to PATH", or use `py -3` instead of `python`.
- Dependencies missing: the script installs them; if it fails, run `pip install flask flask-cors` or `py -3 -m pip install flask flask-cors`.

### Using the start script (recommended)
```cmd
start_web_windows.bat
```
After success, the browser opens `http://127.0.0.1:15000`. If the port is occupied, follow the prompt to use another port.

### Step 1: Check Python
```cmd
python --version
```
If missing, install from python.org and check "Add Python to PATH".

### Step 2: Go to project directory
```cmd
cd C:\\path\\to\\MonteHoldem\\v2
```

### Step 3: Install dependencies (manual fallback)
```cmd
pip install flask flask-cors
```

### Step 3.5: Manual start (if the script fails)
```cmd
python server.py
```
Or `py -3 server.py`. When you see `PokerWin v2 server: http://127.0.0.1:15000`, open that address.

### Web interface usage
- Visit the shown URL (default `http://127.0.0.1:15000`).
- Select your hand (2 cards) and community cards (0-5 cards).
- Check positions that remain in the pot.
- Set opponent ranges (Tight/Standard/Loose/Random).
- Click "Calculate Equity".

### Command-line tool (Windows)
```cmd
# Basic
python -m pokerwin.cli --hand "Ah Kd" --players 3 --sims 10000

# With board
python -m pokerwin.cli --hand "Ah Kd" --board "Qh Jh Th" --players 4 --sims 10000

# Default opponent range
python -m pokerwin.cli --hand "Ah Kd" --players 3 --sims 10000 --opponent-range tight

# Per-opponent ranges
python -m pokerwin.cli --hand "Ah Kd" --players 4 --opponent-ranges tight loose standard
```

Parameters: same as macOS section above.

---

## 📝 Card Format Reference
- Ranks: `A K Q J T 9 8 7 6 5 4 3 2`
- Suits: `h` Hearts (♥), `d` Diamonds (♦), `s` Spades (♠), `c` Clubs (♣)
- Examples: `Ah` = Ace of Hearts, `Kd` = King of Diamonds, `Qs` = Queen of Spades, `Jc` = Jack of Clubs

---

## 🎯 Opponent Range Definitions
- Random: any two cards
- Tight: TT+, AK, AQ, AJs+, KQs
- Standard: 77+, A2s-AKs, T9s+, AJo+, KQo
- Loose: any pair, suited aces/connectors/one-gappers, ATo+, KJo+

---

## ❓ Troubleshooting
1) "Module 'flask' not found"
```bash
# macOS
pip3 install flask flask-cors
# Windows
pip install flask flask-cors
```

2) Cannot open web page
- Ensure `server.py` is running (terminal shows server address).
- Use `http://127.0.0.1:15000` (not https).
- Make sure firewall is not blocking Python.

3) "No module named pokerwin"
- Ensure current directory is the `v2` folder.
- Use `python -m pokerwin.cli` instead of `python pokerwin/cli.py`.

4) Calculation is slow
- Lower `--sims`, e.g., `--sims 1000`. Web defaults to 10000 and usually finishes in 1-2 seconds.

---

## 📂 Project Structure
```
v2/
├── index.html              # Web interface
├── server.py               # Flask backend server
├── pokerwin/               # Python module
│   ├── __init__.py
│   ├── cli.py              # Command-line entry point
│   ├── simulator.py        # Monte Carlo simulator
│   ├── evaluator.py        # Hand strength evaluator
│   ├── models.py           # Card data structures
│   └── parser.py           # Command-line argument parser
└── tests/                  # Unit tests
```

---

## 🔬 Running Tests (Optional)
If pytest is installed:
```bash
# macOS
pip3 install pytest
pytest -q

# Windows
pip install pytest
pytest -q
```

---

## 📧 Contact
For questions, please contact: [Your Email/Student ID]

**Enjoy using PokerWin! 🎉**

## 📝 Card Format Reference

### Ranks
- `A` = Ace
- `K` = King
- `Q` = Queen
- `J` = Jack
- `T` = Ten (10)
- `9`-`2` = Nine through Two

### Suits
- `h` = Hearts (♥)
- `d` = Diamonds (♦)
- `s` = Spades (♠)
- `c` = Clubs (♣)

### Examples
- `Ah` = Ace of Hearts
- `Kd` = King of Diamonds
- `Qs` = Queen of Spades
- `Jc` = Jack of Clubs

---

## 🎯 Opponent Range Definitions

### Random
Any two cards

### Tight
- Pairs: TT+ (Ten-Ten and above)
- AK, AQ (any suit)
- AJs+, KQs (suited)

### Standard
- Pairs: 77+
- Suited Aces: A2s-AKs
- Suited Connectors: T9s+
- Offsuit Broadways: AJo+, KQo

### Loose
- Any pair
- Suited Aces, suited connectors, suited one-gappers
- ATo+, KJo+

---

## ❓ Troubleshooting

### 1. "Module 'flask' not found"
Run:
```bash
# macOS
pip3 install flask flask-cors

# Windows
pip install flask flask-cors
```

### 2. Cannot open web page
Ensure:
- server.py is running (terminal shows server address)
- Browser visits `http://127.0.0.1:15000` (not https)
- Firewall is not blocking Python

### 3. Command line shows "No module named pokerwin"
Ensure:
- Current directory is in `v2` folder
- Use `python -m pokerwin.cli` instead of `python pokerwin/cli.py`

### 4. Calculation is slow
- Reduce simulations: `--sims 1000`
- Web version defaults to 10000, typically completes in 1-2 seconds

---

## 📂 Project Structure

```
v2/
├── index.html              # Web interface
├── server.py               # Flask backend server
├── pokerwin/               # Python module
│   ├── __init__.py
│   ├── cli.py              # Command-line entry point
│   ├── simulator.py        # Monte Carlo simulator
│   ├── evaluator.py        # Hand strength evaluator
│   ├── models.py           # Card data structures
│   └── parser.py           # Command-line argument parser
└── tests/                  # Unit tests
```

---

## 🔬 Running Tests (Optional)

If pytest is installed:
```bash
# macOS
pip3 install pytest
pytest -q

# Windows
pip install pytest
pytest -q
```

---

## 📧 Contact

For questions, please contact: [Your Email/Student ID]

**Enjoy using PokerWin! 🎉**

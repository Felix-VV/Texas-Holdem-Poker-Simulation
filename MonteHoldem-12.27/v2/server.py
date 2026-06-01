from __future__ import annotations

from typing import Any, List, Optional
import os

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from pokerwin.models import Card
from pokerwin.simulator import calculate_equity_percent

# Standard 6-max Poker table positions
POSITIONS_6MAX = ["UTG", "HJ", "CO", "BTN", "SB", "BB"]

def _normalize_position(p: Any) -> str:
    """
    Standardizes position strings to uppercase and validates against 6-max seats.
    Raises ValueError if the position is not recognized.
    """
    s = str(p).upper().strip()
    if s not in POSITIONS_6MAX:
        raise ValueError(f"Invalid position: {p!r}. Must be one of {POSITIONS_6MAX}.")
    return s

def _parse_in_pool_positions(values: Any) -> List[str]:
    """
    Parses the list of positions currently involved in the pot.
    Ensures they are valid 6-max positions and removes duplicates while preserving order.
    """
    if values is None:
        return []
    if not isinstance(values, list):
        raise ValueError("'in_pool' must be a list of positions")
    
    positions = [_normalize_position(v) for v in values]
    
    # Remove duplicates while preserving original input order
    seen = set()
    out: List[str] = []
    for p in positions:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out

def _parse_card_list(values: Any, *, field: str) -> List[Card]:
    """
    Converts a list of string representations (e.g., ['As', 'Kd']) into Card objects.
    Used for both Hero's hole cards and the community board.
    """
    if values is None:
        return []
    if not isinstance(values, list):
        raise ValueError(f"'{field}' must be a list of card strings")
    return [Card.from_string(str(v)) for v in values]

app = Flask(__name__)
# Enable Cross-Origin Resource Sharing for frontend-backend communication
CORS(app)

@app.post("/calculate")
def calculate() -> Any:
    """
    Main endpoint for equity calculation.
    
    Expects JSON payload with:
    - hero: List[str] (e.g., ["Ah", "Ad"])
    - community/board: List[str]
    - players: int (Must be 6)
    - sims: int (Number of Monte Carlo iterations)
    - hero_pos: str (Hero's seat, e.g., "BTN")
    - in_pool: List[str] (Positions currently active in the hand)
    - ranges_by_pos: Dict[str, str] (Optional mapping of position to range name)
    """
    try:
        data = request.get_json(force=True, silent=False) or {}

        # 1. Parse basic hand data
        hero = _parse_card_list(data.get("hero", []), field="hero")
        board = _parse_card_list(data.get("community", data.get("board", [])), field="community")
        
        # 2. Configuration & Validation
        players = int(data.get("players", 6))
        if players != 6:
            raise ValueError("This app currently supports 6-max only: players must be 6")
        
        sims = int(data.get("sims", 10_000))
        seed_raw: Optional[Any] = data.get("seed", None)
        seed = int(seed_raw) if seed_raw is not None else None
        
        # 3. Position Logic
        hero_pos = _normalize_position(data.get("hero_pos", "BTN"))
        # 'in_pool' defines who hasn't folded PRE-FLOP.
        in_pool = _parse_in_pool_positions(data.get("in_pool", POSITIONS_6MAX))

        # Determine active opponents: Everyone in the pool except Hero.
        active_positions = [p for p in in_pool if p != hero_pos]
        active_opponents_count = len(active_positions)

        # 4. Range Logic
        ranges_by_pos_raw = data.get("ranges_by_pos", None)
        if ranges_by_pos_raw is not None and not isinstance(ranges_by_pos_raw, dict):
            raise ValueError("'ranges_by_pos' must be an object mapping position -> range")

        def get_range_for_pos(pos: str) -> str:
            """Helper to resolve range name for a specific seat."""
            if isinstance(ranges_by_pos_raw, dict) and pos in ranges_by_pos_raw:
                return str(ranges_by_pos_raw[pos])
            return "standard"

        # Construct a list of range strings corresponding to each active opponent seat.
        # This allows the simulator to sample 'Tight' for UTG and 'Wide' for BTN simultaneously.
        opponent_ranges = [get_range_for_pos(p).lower() for p in active_positions]

        # 5. Simulation Execution
        # Note: This simulates Showdown Equity for the specified active players.
        # It assumes these players stay in until the end.
        equity = calculate_equity_percent(
            hero,
            board=board,
            players=players,
            sims=sims,
            seed=seed,
            active_opponents=active_opponents_count,
            opponent_ranges=opponent_ranges,
        )
        
        return jsonify({
            "equity": equity, 
            "win_rate": equity,
            "info": f"Simulated vs {active_opponents_count} opponents"
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Catch-all for server-side errors
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@app.get("/")
def index() -> Any:
    """Serves the main frontend entry point (index.html)."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "index.html")
    return send_file(html_path)

if __name__ == "__main__":
    # Environment variable PORT is used for cloud deployments (e.g., Heroku/Render)
    port = int(os.environ.get("PORT", "15000"))
    print(f"PokerWin v2 server started at: http://127.0.0.1:{port}")
    
    # use_reloader=False prevents the server from restarting twice in some IDEs.
    app.run(port=port, debug=True, use_reloader=False)

    
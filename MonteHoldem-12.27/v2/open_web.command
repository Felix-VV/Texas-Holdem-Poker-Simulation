#!/bin/zsh
set -euo pipefail

# Always run relative to this script's location (portable across machines/folders)
DIR="$(cd "$(dirname "$0")" && pwd)"
PORT="${PORT:-15002}"
VENV_DIR="${VENV_DIR:-"$DIR/.venv"}"
LOG_FILE="/tmp/pokerwin_server_${PORT}.log"

cd "$DIR"

if ! command -v python3 >/dev/null 2>&1; then
	echo "python3 not found. Please install Python 3 first (python.org or Homebrew)."
	exit 1
fi

# Create/Reuse a local virtual environment so this folder is portable
if [[ ! -x "$VENV_DIR/bin/python" ]]; then
	echo "Creating venv at: $VENV_DIR"
	python3 -m venv "$VENV_DIR"
fi

PY="$VENV_DIR/bin/python"

# Install dependencies automatically (only when needed)
REQ_FILE="$DIR/requirements.txt"
REQ_STAMP="$VENV_DIR/.requirements_installed"
if [[ -f "$REQ_FILE" ]]; then
	if [[ ! -f "$REQ_STAMP" || "$REQ_FILE" -nt "$REQ_STAMP" ]]; then
		echo "Installing Python dependencies from requirements.txt ..."
		"$PY" -m pip install --upgrade pip setuptools wheel >/dev/null 2>&1 || true
		"$PY" -m pip install -r "$REQ_FILE"
		touch "$REQ_STAMP"
	fi
else
	echo "Warning: requirements.txt not found; continuing anyway."
fi

# Stop any previous process listening on this port
PIDS="$(lsof -ti tcp:"$PORT" -sTCP:LISTEN 2>/dev/null || true)"
if [[ -n "$PIDS" ]]; then
	kill $PIDS 2>/dev/null || true
	sleep 0.2
fi

# Start server in background
PORT="$PORT" "$PY" server.py >"$LOG_FILE" 2>&1 &
SERVER_PID=$!

echo "Started server (pid=$SERVER_PID) on http://127.0.0.1:${PORT}/"

# Give it a moment to bind
sleep 0.6

# Open system browser
open "http://127.0.0.1:${PORT}/"

echo "If the page doesn't load, check: $LOG_FILE"
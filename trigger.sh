#!/bin/bash
# Trigger recording - uses best method for OS

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Activate venv and run
source "$SCRIPT_DIR/venv/bin/activate"
python3 "$SCRIPT_DIR/main.py" --trigger

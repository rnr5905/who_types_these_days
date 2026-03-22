#!/bin/bash
# Trigger recording - uses best method for OS

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Try signal first (Linux/macOS), fall back to file trigger
python "$SCRIPT_DIR/main.py" --trigger

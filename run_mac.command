#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "======================================================================"
echo "       ZIZIPHUS JUJUBA : SIGNAL INTELLIGENCE & PATTERN LAB"
echo "======================================================================"
echo "Launching local laboratory on macOS..."

if command -v python3 &>/dev/null; then
    python3 run_app.py
elif command -v python &>/dev/null; then
    python run_app.py
else
    echo "[ERROR] Python 3 is required. Please install Python 3."
    read -p "Press [Enter] to exit..."
fi

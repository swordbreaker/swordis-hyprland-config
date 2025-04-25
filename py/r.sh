#!/bin/bash

# Script to run Python files with uv
# Usage: r.sh script.py [arg1 arg2 ...]

if [ $# -eq 0 ]; then
    echo "Usage: $0 <script.py> [arguments]"
    exit 1
fi

# Get the script name from first argument
SCRIPT_NAME=$1
shift  # Remove the first argument (script name) from the arguments list

# Change to the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Run the Python script using uv, passing all remaining arguments
uv run "$SCRIPT_NAME" "$@"
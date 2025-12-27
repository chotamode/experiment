#!/bin/bash
# Quick Start Script for Kanji Collage Generator
# Usage: ./run.sh [optional arguments for main.py]

set -e

VENV_DIR=".venv"

echo "🎨 Kanji Collage Generator - Quick Start"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 First-time setup: Creating virtual environment..."
    python3 -m venv "$VENV_DIR"

    echo "📥 Installing dependencies..."
    "$VENV_DIR/bin/pip" install --quiet --upgrade pip
    "$VENV_DIR/bin/pip" install --quiet -r requirements.txt

    echo "✅ Setup complete!"
    echo ""
fi

# Run the application
echo "🚀 Running Kanji Collage Generator..."
echo ""

"$VENV_DIR/bin/python" main.py "$@"

echo ""
echo "✨ Done! Check the downloads/ folder for your collage."

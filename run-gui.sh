#!/bin/bash
# GUI Launcher for Kanji Collage Generator (Linux/Mac)

set -e

VENV_DIR=".venv"

echo "🎨 Kanji Collage Generator - GUI"
echo "================================"
echo ""

# Check for tkinter (required for GUI on Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if ! python3 -c "import tkinter" &> /dev/null; then
        echo "⚠️  tkinter is not installed!"
        echo ""
        echo "On Linux, tkinter needs to be installed separately:"
        echo ""
        echo "Ubuntu/Debian:"
        echo "  sudo apt install python3-tk"
        echo ""
        echo "Fedora:"
        echo "  sudo dnf install python3-tkinter"
        echo ""
        echo "Arch:"
        echo "  sudo pacman -S tk"
        echo ""
        echo "After installing, run this script again."
        echo ""
        exit 1
    fi
fi

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 First-time setup: Creating virtual environment..."

    # Check if uv is available (10-100x faster than pip!)
    if command -v uv &> /dev/null; then
        echo "⚡ Using uv (ultra-fast mode!)..."
        uv venv "$VENV_DIR"
        echo "📥 Installing dependencies with uv..."
        uv pip install -r requirements.txt --python "$VENV_DIR/bin/python"
    else
        echo "📥 Installing with pip (tip: install 'uv' for 10x faster setup!)..."
        python3 -m venv "$VENV_DIR"
        "$VENV_DIR/bin/pip" install --quiet --upgrade pip
        "$VENV_DIR/bin/pip" install --quiet -r requirements.txt
    fi

    echo "✅ Setup complete!"
    echo ""
fi

# Run the GUI
echo "🚀 Launching GUI..."
"$VENV_DIR/bin/python" gui.py

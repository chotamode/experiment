# ⚡ Quick Start Guide

**Run in seconds without manual installation!**

## 📋 System Requirements (Linux GUI Users Only)

**If you're using the GUI on Linux**, you need to install tkinter first:

**Ubuntu/Debian:**
```bash
sudo apt install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**Arch:**
```bash
sudo pacman -S tk
```

**macOS/Windows:** tkinter is included with Python, no extra steps needed!

**Don't want to install tkinter?** Use the command-line mode instead (see below).

---

## 🖼️ GUI Mode (Recommended - Most User-Friendly)

### Linux/Mac:
```bash
./run-gui.sh
```

### Windows:
```batch
run-gui.bat
```

**Features:**
- 🎨 Beautiful graphical interface
- 🎯 Built-in quick presets (Quick Test, Chaos Mode, Clean Grid, Wallpaper)
- 📊 Real-time progress and logs
- 🔧 Easy settings with sliders and dropdowns
- 📁 One-click folder opening
- No command-line knowledge needed!

---

## 💻 Command-Line Mode (For Advanced Users)

### Linux/Mac:
```bash
./run.sh
```

### Windows:
```batch
run.bat
```

**What happens:**
- ✅ Auto-create a virtual environment (first time only)
- ✅ Auto-install all dependencies (first time only)
- ✅ Run the app immediately
- ✅ Subsequent runs are instant!

**First run**: ~30 seconds with pip, or **2-3 seconds with uv** (see below)
**After that**: Instant! ⚡

---

## ⚡ **ULTRA FAST**: Install with `uv` (10-100x faster!)

Install `uv` for blazing-fast dependency installation:

**Linux/Mac:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Then run normally:**
```bash
./run-gui.sh  # or ./run.sh
```

The script automatically detects and uses `uv` if available!

**Speed comparison:**
- With pip: ~30 seconds first install
- With uv: **~2-3 seconds** ⚡⚡⚡

## 📝 With Custom Options

Pass any arguments just like normal:

### Linux/Mac:
```bash
./run.sh -q 10 -t mosaic -e 5
./run.sh -k nonsense -t scattered
./run.sh --help
```

### Windows:
```batch
run.bat -q 10 -t mosaic -e 5
run.bat -k nonsense -t scattered
run.bat --help
```

## 🎯 Quick Presets

**Chaos mode** (pure random kanji, heavy effects):
```bash
./run.sh -k nonsense -t scattered -e 5 -q 10
```

**Fast test** (small size, few images):
```bash
./run.sh -q 3 -m 10 -s 1200
```

**Large wallpaper** (3000x3000px, many images):
```bash
./run.sh -q 10 -m 80 -s 3000 -t mosaic
```

**Clean grid** (no effects, organized layout):
```bash
./run.sh -t grid --no-effects
```

## 🔧 Alternative: Manual Install

If you prefer manual installation:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

## 💡 One-Liner (No Virtual Environment)

**Use only if you don't care about system packages:**

```bash
pip install -r requirements.txt && python main.py
```

⚠️ Not recommended: installs packages globally

## 📦 What Gets Installed

Only 5 lightweight packages:
- **Pillow** (image manipulation)
- **requests** (HTTP requests)
- **rich** (pretty CLI output)
- **duckduckgo-search** (image search)
- **numpy** (array operations)

Total download: ~15-20 MB

## 🎨 Example Workflow

```bash
# Clone or download the project
git clone <repo-url>
cd kanji-collage-generator

# Run it! (first time auto-installs)
./run.sh

# Try different styles
./run.sh -k nonsense -t scattered -e 5
./run.sh -t mosaic -q 10
./run.sh -k themed -t grid

# Check your creations
ls downloads/
```

## ❓ Troubleshooting

**Permission denied on Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Python not found:**
- Install Python 3.8+ from python.org
- Or use `python` instead of `python3`

**Slow first run:**
- Normal! Dependencies are downloading
- Subsequent runs are instant

**No images found:**
- Try different kanji mode: `./run.sh -k auto`
- Increase queries: `./run.sh -q 10`

---

**That's it! You're ready to create surreal art! 🎨✨**

Check `downloads/` folder for your collages after each run.

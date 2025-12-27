@echo off
REM GUI Launcher for Kanji Collage Generator (Windows)

setlocal enabledelayedexpansion

set VENV_DIR=.venv

echo 🎨 Kanji Collage Generator - GUI
echo ================================
echo.

REM Check if virtual environment exists
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo 📦 First-time setup: Creating virtual environment...

    REM Check if uv is available (10-100x faster than pip!)
    where uv >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo ⚡ Using uv (ultra-fast mode!)...
        uv venv %VENV_DIR%
        echo 📥 Installing dependencies with uv...
        uv pip install -r requirements.txt --python %VENV_DIR%\Scripts\python.exe
    ) else (
        echo 📥 Installing with pip (tip: install 'uv' for 10x faster setup!)...
        python -m venv %VENV_DIR%
        %VENV_DIR%\Scripts\python.exe -m pip install --quiet --upgrade pip
        %VENV_DIR%\Scripts\python.exe -m pip install --quiet -r requirements.txt
    )

    echo ✅ Setup complete!
    echo.
)

REM Run the GUI
echo 🚀 Launching GUI...
%VENV_DIR%\Scripts\pythonw.exe gui.py

endlocal

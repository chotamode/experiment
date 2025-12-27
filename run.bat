@echo off
REM Quick Start Script for Kanji Collage Generator (Windows)
REM Usage: run.bat [optional arguments for main.py]

setlocal enabledelayedexpansion

set VENV_DIR=.venv

echo 🎨 Kanji Collage Generator - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo 📦 First-time setup: Creating virtual environment...
    python -m venv %VENV_DIR%

    echo 📥 Installing dependencies...
    %VENV_DIR%\Scripts\python.exe -m pip install --quiet --upgrade pip
    %VENV_DIR%\Scripts\python.exe -m pip install --quiet -r requirements.txt

    echo ✅ Setup complete!
    echo.
)

REM Run the application
echo 🚀 Running Kanji Collage Generator...
echo.

%VENV_DIR%\Scripts\python.exe main.py %*

echo.
echo ✨ Done! Check the downloads\ folder for your collage.

endlocal

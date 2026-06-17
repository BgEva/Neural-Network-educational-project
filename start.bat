@echo off
cd /d "%~dp0"
echo ========================
echo Game Chatbot Setup
echo ========================
echo.
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found!
    echo Install Python from python.org
    echo Make sure to check "Add Python to PATH"
    pause
    exit
)
echo Python found!
echo.
echo Installing libraries...
python -m pip install -r requirements.txt
echo.
echo Starting chatbot...
python chatbot.py
pause
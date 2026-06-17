@echo off
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Install from python.org
    pause
    exit
)
echo Installing libraries...
python -m pip install -r requirements.txt
echo Starting chatbot...
python chatbot.py
pause
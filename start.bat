@echo off
cd /d "%~dp0"
echo ========================
echo AI Labs Launcher
echo ========================
echo.
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found!
    echo.
    echo Download Python from https://python.org
    echo During install check "Add Python to PATH"
    echo.
    pause
    exit
)
echo Python found!
echo.
echo 1. Game Chatbot (Neural + Graph)
echo 2. Semantic Search
echo 3. AND/OR Graph
echo 4. Install Requirements
echo 5. Exit
echo.
set /p choice="Choose (1-5): "

if "%choice%"=="1" (
    echo Starting Chatbot...
    python chatbot.py
    pause
    goto menu
)
if "%choice%"=="2" (
    echo Starting Semantic Search...
    python semantic_search.py
    pause
    goto menu
)
if "%choice%"=="3" (
    echo Starting AND/OR Graph...
    python and_or_graph.py
    pause
    goto menu
)
if "%choice%"=="4" (
    echo Installing libraries...
    python -m pip install -r requirements.txt
    pause
    goto menu
)
if "%choice%"=="5" exit
goto menu
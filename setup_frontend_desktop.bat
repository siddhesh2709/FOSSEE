@echo off
echo ================================================
echo Chemical Equipment Visualizer - Desktop App Setup
echo ================================================
echo.

cd frontend-desktop

echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ================================================
echo Setup complete!
echo.
echo Next steps:
echo 1. Make sure backend is running
echo 2. Run the desktop app: python main.py
echo ================================================
echo.

pause

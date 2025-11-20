@echo off
echo ================================================
echo Starting PyQt5 Desktop Application
echo ================================================
echo.

cd frontend-desktop
call venv\Scripts\activate.bat
python main.py

pause

@echo off
echo ================================================
echo Starting Django Backend Server
echo ================================================
echo.

cd backend
call venv\Scripts\activate.bat
python manage.py runserver

pause

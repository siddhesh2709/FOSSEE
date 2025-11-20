@echo off
echo ================================================
echo Chemical Equipment Visualizer - Backend Setup
echo ================================================
echo.

cd backend

echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Running migrations...
python manage.py migrate

echo.
echo ================================================
echo Setup complete!
echo.
echo Next steps:
echo 1. Create a superuser: python manage.py createsuperuser
echo 2. Start the server: python manage.py runserver
echo ================================================
echo.

pause

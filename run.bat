@echo off
REM Activating the virtual environment
call venv\Scripts\activate

REM Running the FastAPI application
python app/main.py

REM Optionally, keep the terminal open after execution
pause

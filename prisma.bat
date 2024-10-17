@echo off
REM Activating the virtual environment
call venv\Scripts\activate

REM Running the FastAPI application
cd app/ && prisma studio

REM Optionally, keep the terminal open after execution
pause

@echo off
REM Activating the virtual environment
source venv/Scripts/activate && cd app/ && prisma studio

REM Running the FastAPI application


REM Optionally, keep the terminal open after execution
pause

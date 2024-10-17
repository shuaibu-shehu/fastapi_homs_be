@echo off
REM Activating the virtual environment
call venv\Scripts\activate

cd app
npx prisma studio
REM Optionally, keep the terminal open after execution
pause

@echo off

echo ================================
echo        PocketSmart AI
echo ================================
echo.

echo Starting PocketSmart AI backend...
echo.

call venv\Scripts\activate

uvicorn backend.server:app --reload

pause
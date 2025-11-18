@echo off
echo ========================================
echo  Clinical Case Platform - Startup
echo ========================================
echo.
echo Starting Backend and Frontend servers...
echo.
echo Backend will run on: http://localhost:8000
echo Frontend will run on: http://localhost:5173
echo.
echo Press Ctrl+C to stop all servers
echo ========================================
echo.

:: Start backend in new window
start "Django Backend - Port 8000" cmd /k "cd /d %~dp0backend && python manage.py runserver"

:: Wait 3 seconds for backend to start
timeout /t 3 /nobreak >nul

:: Start frontend in new window  
start "Vue Frontend - Port 5173" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo  Both servers are starting...
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Close this window when done (servers will keep running)
echo Or close individual server windows to stop them
<
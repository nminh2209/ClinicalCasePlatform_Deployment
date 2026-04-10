@echo off
echo ========================================
echo  Clinical Case Platform - Shutdown
echo ========================================
echo.

:: Stop backend Docker containers
echo [1/2] Stopping backend Docker containers...
cd /d %~dp0backend
docker compose down
echo Backend containers stopped.
echo.

:: Kill frontend dev server (node/vite on port 5173)
echo [2/2] Stopping frontend dev server...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5173 " ^| findstr "LISTENING"') do (
    echo Stopping process %%a on port 5173
    taskkill /PID %%a /F >nul 2>&1
)
echo Frontend stopped.
echo.

echo ========================================
echo  All servers stopped.
echo ========================================

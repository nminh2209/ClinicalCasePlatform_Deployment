@echo off
echo ========================================
echo  Clinical Case Platform - Startup
echo ========================================
echo.
echo Backend (Docker): http://localhost:8000
echo Frontend (Vite):  http://localhost:5173
echo.
echo Press Ctrl+C to stop all servers
echo ========================================
echo.

:: Start backend Docker containers (postgres, redis, backend)
echo [1/2] Starting backend Docker containers...
start "Docker Backend" cmd /k "cd /d %~dp0backend && docker compose up --build"

:: Wait for Docker services to begin starting
timeout /t 5 /nobreak >nul

:: Start frontend dev server
echo [2/2] Starting frontend dev server...
start "Vue Frontend - Port 5173" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo  Both servers are starting...
echo ========================================
echo.
echo Backend (Docker): http://localhost:8000
echo   - PostgreSQL:   localhost:5432
echo   - Redis:        localhost:6379
echo Frontend (Vite):  http://localhost:5173
echo.
echo Close individual windows to stop them,
echo or run stop_all.bat to shut everything down.

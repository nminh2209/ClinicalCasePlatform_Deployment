@echo off
REM Start Django server with Daphne (ASGI for WebSocket support)
REM Make sure Redis is running: redis-server

cd /d "%~dp0"

echo Starting Clinical Case Platform with WebSocket support...
echo Make sure Redis is running on localhost:6379
echo.

daphne -b 0.0.0.0 -p 8000 clinical_case_platform.asgi:application

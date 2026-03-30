@echo off
REM Quick Database Reset Script for Windows
REM This script resets the database and repopulates it with test data

echo ========================================
echo Clinical Case Platform - Database Reset
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found!
    echo Please create a virtual environment first:
    echo   python -m venv venv
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Run reset script
echo.
echo Running database reset script...
echo.
python reset_database.py

REM Check if successful
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Database reset completed successfully!
    echo ========================================
    echo.
    echo You can now login with:
    echo   Admin: admin@test.com / minh1234minh
    echo   Instructor: instructor@test.com / testpass123
    echo   Student: student@test.com / testpass123
    echo.
) else (
    echo.
    echo ========================================
    echo Error occurred during database reset!
    echo ========================================
    echo.
)

pause

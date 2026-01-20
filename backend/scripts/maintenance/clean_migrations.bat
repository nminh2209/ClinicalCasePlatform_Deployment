@echo off
REM Clean Migration Reset Script
REM This script resets migrations by keeping models but recreating migration history

echo ========================================
echo MIGRATION CLEANUP SCRIPT
echo ========================================
echo.
echo WARNING: This will reset migration history!
echo Make sure you have a backup of your database.
echo.
set /p confirm="Type 'yes' to continue: "

if not "%confirm%"=="yes" (
    echo Cancelled.
    exit /b
)

echo.
echo Step 1: Recording current database state...
python manage.py migrate --fake

echo.
echo Step 2: Deleting all migration files (keeping __init__.py)...

REM Delete migration files but keep __init__.py
for /d %%D in (accounts cases comments exports feedback grades repositories templates) do (
    if exist %%D\migrations (
        echo Cleaning %%D migrations...
        for %%F in (%%D\migrations\*.py) do (
            if not "%%~nxF"=="__init__.py" (
                del "%%F"
            )
        )
        if exist %%D\migrations\__pycache__ (
            rmdir /s /q "%%D\migrations\__pycache__"
        )
    )
)

echo.
echo Step 3: Creating fresh migrations...
python manage.py makemigrations

echo.
echo Step 4: Marking new migrations as applied (fake)...
python manage.py migrate --fake

echo.
echo ========================================
echo MIGRATION CLEANUP COMPLETE!
echo ========================================
echo.
echo All apps now have single, clean initial migrations.
echo Database unchanged, but migration history is clean.
echo.
pause

@echo off
echo ========================================
echo   DATABASE RESET AND POPULATION
echo ========================================
echo.
echo WARNING: This will DELETE ALL DATA!
echo.
set /p confirm="Are you sure? (yes/no): "
if /i NOT "%confirm%"=="yes" (
    echo Operation cancelled.
    exit /b 1
)

echo.
echo 1. Dropping database...
python reset_database.py

echo.
echo 2. Running migrations...
python manage.py migrate

echo.
echo 3. Populating comprehensive test data...
python populate_test_data.py --clear-existing

echo.
echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo You can now login with:
echo   Admin: admin@test.com / minh1234minh
echo   Instructor: instructor@test.com / testpass123
echo   Student: student@test.com / testpass123
echo.
pause

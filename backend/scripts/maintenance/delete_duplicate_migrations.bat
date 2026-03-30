@echo off
REM Delete problematic duplicate migration files

echo ========================================
echo DELETING DUPLICATE MIGRATIONS
echo ========================================
echo.

echo Deleting cases app duplicates...
if exist "cases\migrations\0007_merge_20251110_1158.py" del "cases\migrations\0007_merge_20251110_1158.py"
if exist "cases\migrations\0009_merge_20251111_1015.py" del "cases\migrations\0009_merge_20251111_1015.py"
if exist "cases\migrations\0009_icd10code_medicalabbreviation_caseanalytics_and_more.py" del "cases\migrations\0009_icd10code_medicalabbreviation_caseanalytics_and_more.py"
if exist "cases\migrations\0012_merge_20251115_1347.py" del "cases\migrations\0012_merge_20251115_1347.py"

echo Deleting exports app duplicates...
if exist "exports\migrations\0002_caseexport_completed_at_caseexport_error_message_and_more.py" del "exports\migrations\0002_caseexport_completed_at_caseexport_error_message_and_more.py"
if exist "exports\migrations\0003_merge_20251115_1346.py" del "exports\migrations\0003_merge_20251115_1346.py"

echo.
echo Deleting __pycache__ files...
if exist "cases\migrations\__pycache__\0007_merge_20251110_1158.*.pyc" del "cases\migrations\__pycache__\0007_merge_20251110_1158.*.pyc"
if exist "cases\migrations\__pycache__\0009_*.pyc" del "cases\migrations\__pycache__\0009_*.pyc"
if exist "cases\migrations\__pycache__\0012_*.pyc" del "cases\migrations\__pycache__\0012_*.pyc"
if exist "exports\migrations\__pycache__\0002_caseexport_completed_at*.pyc" del "exports\migrations\__pycache__\0002_caseexport_completed_at*.pyc"
if exist "exports\migrations\__pycache__\0003_*.pyc" del "exports\migrations\__pycache__\0003_*.pyc"

echo.
echo ========================================
echo DONE! Now drop the database in pgAdmin
echo Then run: python manage.py migrate
echo ========================================
pause

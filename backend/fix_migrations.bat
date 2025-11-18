@echo off
REM Fix for "relation already exists" error
REM This marks problem migrations as fake (already applied) without running them

echo Fixing migration issues...
echo.

REM Mark the problematic migration as fake
python manage.py migrate cases 0009_icd10code_medicalabbreviation_caseanalytics_and_more --fake

echo.
echo Now running remaining migrations...
python manage.py migrate

echo.
echo Done! If you still see errors, run: python setup_fresh_database.py
pause

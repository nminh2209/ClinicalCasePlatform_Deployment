#!/bin/bash
cd "$(dirname "$0")/../.."
# Delete problematic duplicate migration files

echo "========================================"
echo "DELETING DUPLICATE MIGRATIONS"
echo "========================================"
echo

echo "Deleting cases app duplicates..."
rm -f "cases/migrations/0007_merge_20251110_1158.py"
rm -f "cases/migrations/0009_merge_20251111_1015.py"
rm -f "cases/migrations/0009_icd10code_medicalabbreviation_caseanalytics_and_more.py"
rm -f "cases/migrations/0012_merge_20251115_1347.py"

echo "Deleting exports app duplicates..."
rm -f "exports/migrations/0002_caseexport_completed_at_caseexport_error_message_and_more.py"
rm -f "exports/migrations/0003_merge_20251115_1346.py"

echo
echo "Deleting __pycache__ files..."
# Using find to handle wildcards safely and delete
find cases/migrations/__pycache__ -name "0007_merge_20251110_1158.*.pyc" -delete 2>/dev/null
find cases/migrations/__pycache__ -name "0009_*.pyc" -delete 2>/dev/null
find cases/migrations/__pycache__ -name "0012_*.pyc" -delete 2>/dev/null
find exports/migrations/__pycache__ -name "0002_caseexport_completed_at*.pyc" -delete 2>/dev/null
find exports/migrations/__pycache__ -name "0003_*.pyc" -delete 2>/dev/null

echo
echo "========================================"
echo "DONE! Now drop the database in pgAdmin"
echo "Then run: python manage.py migrate"
echo "========================================"
read -p "Press any key to continue..."

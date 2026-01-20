#!/bin/bash
cd "$(dirname "$0")/../.."
# Fix all "already exists" migration errors

echo "Fixing migration conflicts..."
echo

echo "Marking problematic migrations as fake (already applied)..."
python manage.py migrate cases 0009_icd10code_medicalabbreviation_caseanalytics_and_more --fake
python manage.py migrate cases 0010_studentengagementmetrics_platformusagestatistics_and_more --fake

echo
echo "Running remaining migrations..."
python manage.py migrate

echo
echo "Done!"
read -p "Press any key to continue..."

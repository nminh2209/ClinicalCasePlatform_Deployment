#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing system dependencies..."
apt-get update && apt-get install -y libmagic1

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

echo "Resetting and populating fresh data..."
python manage.py reset_test_data --skip-confirm || echo "Reset failed, trying fresh populate..."

echo "Populating medical terms..."
python populate_medical_terms.py || echo "Medical terms already populated"

echo "Build completed successfully!"

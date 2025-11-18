#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing system dependencies..."
apt-get update && apt-get install -y libmagic1

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

echo "Populating medical terms..."
python populate_medical_terms || echo "Medical terms already populated"

echo "Populating test data..."
python populate_test_data || echo "Test data already populated"

echo "Build completed successfully!"

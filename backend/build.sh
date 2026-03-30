#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing system dependencies..."
apt-get update && apt-get install -y libmagic1

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setting Django settings module for production..."
export DJANGO_SETTINGS_MODULE=clinical_case_platform.settings_production
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
migration_attempts="${MIGRATION_RETRIES:-5}"
migration_delay="${MIGRATION_RETRY_DELAY_SECONDS:-10}"
migration_success=0

for i in $(seq 1 "$migration_attempts"); do
	echo "Migration attempt $i/$migration_attempts..."
	if python manage.py migrate --noinput; then
		migration_success=1
		break
	fi

	if [ "$i" -lt "$migration_attempts" ]; then
		echo "Migration failed, retrying in ${migration_delay}s..."
		sleep "$migration_delay"
	fi
done

if [ "$migration_success" -ne 1 ]; then
	echo "Database migrations failed after $migration_attempts attempts"
	exit 1
fi

if [ "${RUN_SEED_DATA:-false}" = "true" ]; then
	echo "Seeding data because RUN_SEED_DATA=true..."
	python manage.py reset_test_data --skip-confirm || echo "Reset failed, continuing..."
	python populate_medical_terms.py || echo "Medical terms already populated"
fi

echo "Build completed successfully!"

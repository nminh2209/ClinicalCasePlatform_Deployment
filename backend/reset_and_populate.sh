#!/bin/bash
# Reset and populate database on Render

echo "Resetting database data..."
python manage.py reset_test_data --skip-confirm

echo "Database reset complete!"

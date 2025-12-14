#!/usr/bin/env bash
# Start script for Render.com deployment

export DJANGO_SETTINGS_MODULE=clinical_case_platform.settings_production

# Start gunicorn with production settings
exec gunicorn clinical_case_platform.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -

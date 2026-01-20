# Dockerfile for Clinical Case Platform backend
#
# This container runs the Django/DRF backend (incl. Channels) using daphne.
# It expects PostgreSQL and Redis to be provided as external services
# (e.g. via docker-compose) and configured through environment variables
# such as DATABASE_URL / DB_* and REDIS_URL.

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=1

WORKDIR /app

# System dependencies
# - build-essential, libpq-dev: build C extensions / PostgreSQL client libs
# - libffi-dev, libjpeg-dev, zlib1g-dev, libmagic1: Pillow, python-magic, etc.
# - libcairo2, libpangoft2-1.0-0, libpangocairo-1.0-0, libgdk-pixbuf-2.0-0, libglib2.0-0, shared-mime-info: WeasyPrint HTML→PDF
# - poppler-utils: pdf2image support
# - curl: optional debugging
RUN apt-get update && apt-get install -y \
  build-essential \
  libpq-dev \
  libffi-dev \
  libjpeg-dev \
  zlib1g-dev \
  libmagic1 \
  libcairo2 \
  libpangoft2-1.0-0 \
  libpangocairo-1.0-0 \
  libgdk-pixbuf-2.0-0 \
  libglib2.0-0 \
  shared-mime-info \
  poppler-utils \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project code
COPY . .

# Default environment (can be overridden at runtime)
ENV DJANGO_SETTINGS_MODULE=clinical_case_platform.settings \
  PYTHONPATH=/app \
  # These can/should be overridden when you run the container
  DB_ENGINE=django.db.backends.postgresql \
  DB_NAME=clinical_case_platform \
  DB_USER=postgres \
  DB_PASSWORD=postgres \
  DB_HOST=postgres \
  DB_PORT=5432 \
  REDIS_URL=redis://redis:6379/0

# Create non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# NOTE:
# - This CMD auto-runs migrations on container start for convenience.
# - In production, consider running migrations separately.
# - daphne serves the ASGI app (including WebSocket support via Channels).
CMD ["bash", "-lc", "python manage.py migrate --noinput && python scripts/setup/populate_test_data.py && daphne -b 0.0.0.0 -p 8000 clinical_case_platform.asgi:application"]

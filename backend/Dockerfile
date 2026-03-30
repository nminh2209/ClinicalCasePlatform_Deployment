# Dockerfile for Clinical Case Platform backend
#
# This container runs the Django/DRF backend (incl. Channels) using daphne.
# It expects PostgreSQL and Redis to be provided as external services
# (e.g. via docker-compose) and configured through environment variables
# such as DATABASE_URL / DB_* and REDIS_URL.
#
# AI Features included:
#  - OCR: DocTR (GPU-accelerated detection) + VietOCR (Vietnamese recognition)
#         Fallback: PaddleOCR/PaddleX (table extraction with PPSTRUCTURE engine)
#  - ASR: PhoWhisper-medium (Vietnamese speech recognition) via Hugging Face
#         Model (~1.5 GB) is downloaded on first use and cached in /app/ai/asr/phowhisper/
#  - FTS: py_vncorenlp Vietnamese word segmentation (requires Java, provided below)

# ─────────────────────────────────────────────────────────────────────────────
# Stage 1: Get Java from Eclipse Temurin (for py_vncorenlp / FTS)
# ─────────────────────────────────────────────────────────────────────────────
FROM eclipse-temurin:17-jdk-jammy AS java-base

# ─────────────────────────────────────────────────────────────────────────────
# Stage 2: Python application with Java runtime
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# ── Java (for py_vncorenlp / VnCoreNLP FTS) ──────────────────────────────────
COPY --from=java-base /opt/java/openjdk /opt/java/openjdk
ENV JAVA_HOME=/opt/java/openjdk \
    PATH="${JAVA_HOME}/bin:${PATH}"

# ── System dependencies ────────────────────────────────────────────────────────
# Core build / PostgreSQL:
#   build-essential, libpq-dev
# Pillow / file magic:
#   libjpeg-dev, zlib1g-dev, libmagic1, libffi-dev
# WeasyPrint (HTML → PDF):
#   libcairo2, libpangoft2-1.0-0, libpangocairo-1.0-0,
#   libgdk-pixbuf-2.0-0, libglib2.0-0, shared-mime-info
# PDF conversion (pdf2image):
#   poppler-utils
# OCR – OpenCV runtime (opencv-python-headless needs these):
#   libgl1, libglib2.0-0 (already listed above)
# ASR – audio processing (soundfile / librosa):
#   libsndfile1   ← soundfile Python package requires this
#   ffmpeg        ← librosa uses it to decode mp3/ogg/etc. audio formats
# Misc:
#   curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Build tools and PostgreSQL client
    build-essential \
    libpq-dev \
    # Image & file handling
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    libmagic1 \
    # WeasyPrint (HTML → PDF rendering)
    libcairo2 \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libglib2.0-0 \
    shared-mime-info \
    # PDF processing
    poppler-utils \
    # OCR – OpenCV headless runtime
    libgl1 \
    # ASR – audio processing (required by soundfile & librosa)
    libsndfile1 \
    ffmpeg \
    # Utilities
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── Python dependencies ────────────────────────────────────────────────────────
# Copy requirements first to leverage Docker layer cache:
# requirements.txt changes → reinstall deps; only code changes → skip reinstall.
COPY requirements.txt ./

# Upgrade pip then install all Python dependencies in one layer.
# PaddlePaddle is CPU-only here; swap the index URL for a CUDA wheel if needed.
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# ── Application code ───────────────────────────────────────────────────────────
COPY . .

# ── Writable runtime directories ──────────────────────────────────────────────
# Create directories that are written to at runtime so the non-root user
# has ownership from the start (avoids permission errors on first run).
RUN mkdir -p \
    /app/media \
    /app/media/ocr_figures \
    /app/staticfiles \
    /app/logs \
    /app/ai/asr/phowhisper

# ── Non-root user for security ────────────────────────────────────────────────
RUN useradd -m appuser \
    && chown -R appuser:appuser /app
USER appuser

# ── Default environment variables ─────────────────────────────────────────────
# Override these at runtime (docker-compose env section or -e flags).
ENV DJANGO_SETTINGS_MODULE=clinical_case_platform.settings \
    PYTHONPATH=/app \
    # Database
    DB_ENGINE=django.db.backends.postgresql \
    DB_NAME=clinical_case_platform \
    DB_USER=postgres \
    DB_PASSWORD=postgres \
    DB_HOST=postgres \
    DB_PORT=5432 \
    # Redis / Celery / Channels
    REDIS_URL=redis://redis:6379/0 \
    CELERY_BROKER_URL=redis://redis:6379/0 \
    CELERY_RESULT_BACKEND=redis://redis:6379/0 \
    # AI feature flags
    OCR_ENGINE=DOCTR \
    ASR_ENABLED=true \
    # Hugging Face model cache (PhoWhisper downloaded here at first use)
    TRANSFORMERS_CACHE=/app/ai/asr/phowhisper \
    HF_HOME=/app/ai/asr/phowhisper

EXPOSE 8000

# Run migrations, seed data, then start daphne ASGI server
CMD ["bash", "-lc", \
    "python manage.py migrate --noinput \
    && python scripts/setup/populate_test_data.py \
    && python manage.py rebuild_case_search \
    && python manage.py seed_case_choices \
    && daphne -b 0.0.0.0 -p 8000 clinical_case_platform.asgi:application"]
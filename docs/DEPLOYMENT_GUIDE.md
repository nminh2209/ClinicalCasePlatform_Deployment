# Clinical Case Management Platform - Comprehensive Deployment Guide

> **Purpose**: This guide provides exhaustive step-by-step instructions for deploying the Clinical Case Management Platform on both demonstration (free) platforms and production environments for client delivery.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tech Stack Summary](#2-tech-stack-summary)
3. [System Architecture](#3-system-architecture)
4. [Prerequisites](#4-prerequisites)
5. [Free Platform Deployment Options](#5-free-platform-deployment-options)
6. [Step-by-Step Deployment: Railway (Recommended for Free)](#6-step-by-step-deployment-railway-recommended-for-free)
7. [Step-by-Step Deployment: Render](#7-step-by-step-deployment-render)
8. [Step-by-Step Deployment: Fly.io](#8-step-by-step-deployment-flyio)
9. [Step-by-Step Deployment: Google Cloud Run](#9-step-by-step-deployment-google-cloud-run)
10. [Frontend Deployment (Vercel/Netlify)](#10-frontend-deployment-vercelnetlify)
11. [Client Handoff Guide](#11-client-handoff-guide)
12. [Environment Configuration Reference](#12-environment-configuration-reference)
13. [Troubleshooting](#13-troubleshooting)
14. [Maintenance](#14-maintenance)

---

## 1. Project Overview

### Project Name

**Clinical Case Management Platform** (Hệ thống Quản lý Ca bệnh Lâm sàng)

### Purpose

A comprehensive medical education platform designed for Vietnamese medical students and instructors to create, manage, review, and collaborate on clinical case documentation.

### Key Features

- **User Authentication**: JWT-based auth with email/password, social login (Google, Microsoft OAuth)
- **Role-Based Access**: Students, Instructors, and Administrators with different permissions
- **Clinical Case Management**: Create, edit, share, and grade medical case studies
- **Medical File Attachments**: Support for 16 Vietnamese medical document categories (X-rays, lab results, CT scans, MRIs, etc.)
- **AI-Powered Features**:
  - OCR (Optical Character Recognition) for document digitization
  - ASR (Automatic Speech Recognition) using PhoWhisper for Vietnamese
  - Vietnamese Full-Text Search using VnCoreNLP
- **Real-time Notifications**: WebSocket-based notifications via Django Channels
- **Data Export**: Export cases to PDF, Word, and PowerPoint formats
- **Bilingual Support**: Vietnamese and English interfaces

### Target Users

- Medical students documenting clinical cases
- Instructors reviewing and grading student cases
- System administrators managing users and departments

---

## 2. Tech Stack Summary

### Frontend

| Technology  | Version | Purpose                   |
| ----------- | ------- | ------------------------- |
| Vue.js      | 3.5.x   | Core frontend framework   |
| TypeScript  | 5.9.x   | Type safety               |
| Vite        | 7.1.x   | Build tool and dev server |
| Pinia       | 3.0.x   | State management          |
| Vue Router  | 4.5.x   | Client-side routing       |
| PrimeVue    | 4.5.x   | UI component library      |
| TailwindCSS | 4.1.x   | Utility-first CSS         |
| Axios       | 1.12.x  | HTTP client               |
| Vue I18n    | 11.1.x  | Internationalization      |
| Recharts    | 3.4.x   | Data visualization        |

### Backend

| Technology            | Version | Purpose                          |
| --------------------- | ------- | -------------------------------- |
| Django                | 5.1.x   | Core web framework               |
| Django REST Framework | 3.15.x  | REST API                         |
| Django Channels       | 4.0.x   | WebSocket support                |
| PostgreSQL            | 16      | Primary database                 |
| Redis                 | 7       | Caching, Celery broker, Channels |
| Celery                | 5.4.x   | Background task queue            |
| Gunicorn              | 21.2.x  | WSGI server                      |
| Daphne                | 4.1.x   | ASGI server (for Channels)       |
| WhiteNoise            | 6.6.x   | Static file serving              |

### AI/ML Dependencies

| Technology             | Purpose                     |
| ---------------------- | --------------------------- |
| PaddlePaddle/PaddleOCR | OCR with table extraction   |
| python-docx            | Vietnamese OCR recognition  |
| VietOCR                | Vietnamese text recognition |
| Transformers           | PhoWhisper ASR model        |
| Torch                  | ML framework                |
| VnCoreNLP              | Vietnamese NLP/segmentation |
| Sentence-Transformers  | Semantic search             |

### Infrastructure

| Technology     | Purpose                       |
| -------------- | ----------------------------- |
| Docker         | Containerization              |
| Docker Compose | Multi-container orchestration |
| GitHub Actions | CI/CD (optional)              |

---

## 3. System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                │
│                    (Browser / Mobile Web App)                           │
│                  Vue.js SPA with Pinia Store                            │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │ HTTPS
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           CDN / LOAD BALANCER                           │
│                    (Cloudflare / Platform CDN)                           │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
┌───────────────────────────┐    ┌───────────────────────────────┐
│      FRONTEND SERVER      │    │       BACKEND SERVER          │
│         (Vercel)          │    │        (Railway/Render)        │
│                           │    │                               │
│  - Static asset hosting   │    │  - Django + DRF API           │
│  - Edge caching           │    │  - Daphne ASGI (WebSocket)     │
│  - Auto-scaling           │    │  - Gunicorn WSGI fallback     │
│                           │    │  - Celery Worker (background)  │
└───────────────────────────┘    └───────────────────────┬─────────┘
                                                        │
                              ┌─────────────────────────┼─────────────────────────┐
                              │                         │                         │
                              ▼                         ▼                         ▼
                    ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
                    │   POSTGRESQL    │      │      REDIS      │      │    AI MODELS    │
                    │   (Database)    │      │   (Cache/Broker)│      │ (OCR/ASR/FTS)  │
                    │                 │      │                 │      │                 │
                    │  - Cases       │      │  - Session      │      │  - PhoWhisper   │
                    │  - Users       │      │  - Cache        │      │  - VietOCR      │
                    │  - Attachments  │      │  - Channels     │      │  - VnCoreNLP    │
                    │  - Grades      │      │  - Celery       │      │                 │
                    └─────────────────┘      └─────────────────┘      └─────────────────┘
```

### Backend Application Structure

```
backend/
├── clinical_case_platform/          # Django project settings
│   ├── settings.py                  # Standard settings
│   ├── settings_production.py       # Production overrides
│   ├── settings_test.py             # Test environment
│   ├── urls.py                      # Root URL configuration
│   ├── asgi.py                      # ASGI application (WebSocket)
│   ├── wsgi.py                      # WSGI application
│   └── celery.py                    # Celery configuration
├── accounts/                         # User authentication & management
│   ├── models.py                    # Custom User model
│   ├── views.py                     # Auth endpoints
│   ├── serializers.py               # User serialization
│   └── urls.py                      # Auth routes
├── cases/                           # Clinical case management
│   ├── models.py                    # Case, Attachment models
│   ├── views.py                     # Case CRUD endpoints
│   ├── serializers.py              # Case serialization
│   ├── permissions.py              # Case access control
│   └── tasks.py                    # Celery tasks
├── comments/                        # Case commenting system
├── feedback/                        # Student feedback
├── grades/                          # Grading system
├── exports/                         # PDF/Word/PPT export
├── notifications/                   # Real-time notifications
│   ├── consumers.py                 # WebSocket consumers
│   └── routing.py                   # WebSocket routes
├── repositories/                    # File storage
├── inquiries/                       # User inquiries
├── ai/                              # AI/ML features
│   ├── ocr/                         # OCR services
│   │   ├── ocr_service.py           # OCR processing
│   │   ├── views.py                 # OCR API endpoints
│   │   └── tasks.py                 # Async OCR tasks
│   └── asr/                         # Speech recognition
│       ├── service.py               # PhoWhisper service
│       └── views.py                 # ASR endpoints
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker image
└── docker-compose.yml              # Local dev orchestration
```

### Frontend Application Structure

```
frontend/
├── src/
│   ├── main.ts                      # App entry point, router config
│   ├── App.vue                      # Root component
│   ├── views/                        # Page components
│   │   ├── Home.vue                 # Dashboard
│   │   ├── Cases.vue                # Case listing
│   │   ├── CreateCase.vue           # Case wizard
│   │   ├── CaseNotes.vue            # Case detail
│   │   ├── Login.vue                # Authentication
│   │   └── ...
│   ├── components/                  # Reusable components
│   ├── stores/                      # Pinia stores
│   │   ├── auth.ts                  # Auth state
│   │   └── cases.ts                # Cases state
│   ├── services/                    # API service layer
│   │   ├── api.ts                   # Axios config
│   │   ├── auth.ts                 # Auth API calls
│   │   ├── cases.ts                # Case API calls
│   │   └── ocr.ts                  # OCR API calls
│   ├── composables/                 # Vue composables
│   └── utils/                      # Utilities
├── public/                          # Static assets
├── package.json                     # Node dependencies
├── vite.config.ts                   # Vite configuration
└── .env.development                # Dev environment
```

### Data Models

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│       User      │     │      Case       │     │   Attachment    │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)         │────<│ id (PK)         │────<│ id (PK)         │
│ email           │     │ title           │     │ case_id (FK)    │
│ password        │     │ author_id (FK)  │     │ file            │
│ role            │     │ specialty        │     │ category        │
│ student_id      │     │ complexity      │     │ is_confidential │
│ employee_id     │     │ status          │     │ uploaded_by     │
│ department_id   │     │ patient_info    │     │ created_at      │
└─────────────────┘     │ clinical_data   │     └─────────────────┘
        │               └─────────────────┘
        │                       │
        │                       │
        ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Comment      │     │      Grade      │     │   Notification  │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)         │     │ id (PK)         │     │ id (PK)         │
│ case_id (FK)    │     │ case_id (FK)    │     │ user_id (FK)    │
│ author_id (FK)  │     │ reviewer_id(FK) │     │ type            │
│ content         │     │ score           │     │ message         │
│ created_at      │     │ feedback        │     │ is_read         │
└─────────────────┘     │ created_at      │     │ created_at      │
                        └─────────────────┘     └─────────────────┘
```

### API Endpoints Summary

| Category      | Endpoint                       | Methods          | Description          |
| ------------- | ------------------------------ | ---------------- | -------------------- |
| Auth          | `/api/auth/login/`             | POST             | User login           |
| Auth          | `/api/auth/register/`          | POST             | User registration    |
| Auth          | `/api/auth/token/refresh/`     | POST             | JWT refresh          |
| Auth          | `/api/auth/google/`            | POST             | Google OAuth         |
| Auth          | `/api/auth/microsoft/`         | POST             | Microsoft OAuth      |
| Cases         | `/api/cases/`                  | GET, POST        | List/Create cases    |
| Cases         | `/api/cases/{id}/`             | GET, PUT, DELETE | Case CRUD            |
| Cases         | `/api/cases/{id}/attachments/` | GET, POST        | Case attachments     |
| Cases         | `/api/cases/{id}/comments/`    | GET, POST        | Case comments        |
| Cases         | `/api/cases/{id}/grade/`       | GET, POST        | Case grading         |
| Cases         | `/api/cases/search/`           | GET              | Full-text search     |
| OCR           | `/api/ocr/process/`            | POST             | Process document OCR |
| ASR           | `/api/asr/transcribe/`         | POST             | Audio transcription  |
| Notifications | WebSocket `/ws/notifications/` | -                | Real-time updates    |
| Export        | `/api/exports/generate/`       | POST             | Generate export file |

---

## 4. Prerequisites

### System Requirements

| Component  | Minimum | Recommended |
| ---------- | ------- | ----------- |
| Python     | 3.10    | 3.12        |
| Node.js    | 18.x    | 20.x+       |
| PostgreSQL | 14      | 16          |
| Redis      | 6       | 7           |
| RAM        | 4 GB    | 8 GB        |
| Disk       | 10 GB   | 20 GB       |

### Required Accounts

For free deployment, you may need accounts on:

1. **Railway** (Recommended for backend)
   - Sign up at: <https://railway.app>
   - Free tier: 500 hours/month, 1GB RAM, shared CPU

2. **Render** (Alternative for backend)
   - Sign up at: <https://render.com>
   - Free tier: 750 hours/month, 512MB RAM, sleeps after 15min

3. **Fly.io** (Alternative for backend)
   - Sign up at: <https://fly.io>
   - Free tier: 3 shared VMs, 160GB outbound

4. **Vercel** (Frontend)
   - Sign up at: <https://vercel.com>
   - Free tier: Unlimited projects, 100GB bandwidth

5. **Neon** (Free PostgreSQL)
   - Sign up at: <https://neon.tech>
   - Free tier: 0.5GB storage, 1 project

6. **Upstash** (Free Redis)
   - Sign up at: <https://upstash.com>
   - Free tier: 10K commands/day, 256MB

### Local Development Tools

```bash
# Git
git --version

# Python (3.10+)
python --version

# Node.js (18+)
node --version

# Docker (optional but recommended)
docker --version
docker-compose --version

# PostgreSQL client
psql --version
```

---

## 5. Free Platform Deployment Options

### Option Comparison

| Platform    | Backend Support           | Free PostgreSQL    | Free Redis         | Auto-scaling | WebSocket |
| ----------- | ------------------------- | ------------------ | ------------------ | ------------ | --------- |
| **Railway** | ✅ Excellent              | ❌ External needed | ❌ External needed | ✅ Yes       | ✅ Yes    |
| **Render**  | ✅ Good                   | ✅ Built-in        | ❌ External needed | ⚠️ Limited   | ✅ Yes    |
| **Fly.io**  | ✅ Good                   | ✅ External needed | ✅ External needed | ✅ Yes       | ✅ Yes    |
| **Vercel**  | ❌ Backend not supported  | N/A                | N/A                | ✅ Yes       | ❌ No     |
| **Neon**    | Works with Railway/Render | ✅ Native          | N/A                | ✅ Yes       | N/A       |
| **Upstash** | Works with any platform   | N/A                | ✅ Native          | ✅ Yes       | ✅ Yes    |

### Recommended Architecture for Free Deployment

```
┌──────────────────────────────────────────────────────────────────┐
│                        FREE ARCHITECTURE                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐        ┌──────────────────────────────────┐  │
│   │   Vercel     │        │          Railway                 │  │
│   │  (Frontend)  │───────▶│         (Backend)               │  │
│   │              │ HTTPS  │                                  │  │
│   │ - Static     │        │ - Django API                     │  │
│   │   hosting    │        │ - Daphne (WebSocket)             │  │
│   │ - Edge CDN   │        │ - Celery Worker                 │  │
│   └──────────────┘        └──────────────┬───────────────────┘  │
│                                          │                        │
│                                          │                        │
│                    ┌─────────────────────┼─────────────────────┐ │
│                    │                     │                     │ │
│                    ▼                     ▼                     ▼ │
│            ┌──────────────┐    ┌─────────────────┐   ┌────────────┐│
│            │    Neon       │    │    Upstash      │   │ Hugging    ││
│            │ (PostgreSQL)  │    │    (Redis)     │   │    Face    ││
│            │              │    │                │   │  (Models)  ││
│            │ 0.5GB free   │    │ 10K req/day   │   │  (Cached)  ││
│            └──────────────┘    └─────────────────┘   └────────────┘│
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6. Step-by-Step Deployment: Railway (Recommended for Free)

Railway offers the best free tier for hosting the backend with persistent storage and easy scaling.

### Step 6.1: Prepare the Repository

1. **Fork or clone the repository:**

```bash
git clone https://github.com/your-org/clinical-case-platform.git
cd clinical-case-platform/backend
```

1. **Review and update environment variables:**

Create a `.env.production` file:

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-super-secret-production-key-min-50-chars
ALLOWED_HOSTS=your-railway-domain.railway.app,your-frontend.vercel.app

# Database (will be configured via Railway dashboard)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=clinical_case_platform
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=your-neon-host.neon.tech
DB_PORT=5432

# Redis (Upstash)
REDIS_URL=redis://default:your-password@your-redis.upstash.io:6379
CELERY_BROKER_URL=redis://default:your-password@your-redis.upstash.io:6379
CELERY_RESULT_BACKEND=redis://default:your-password@your-redis.upstash.io:6379

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:5173

# AI Features (optional, set to false if not using)
ASR_ENABLED=false
OCR_ENGINE=DOCTR

# Frontend URL
FRONTEND_URL=https://your-frontend.vercel.app
```

### Step 6.2: Set Up Neon PostgreSQL

1. **Create Neon Account:**
   - Go to <https://neon.tech>
   - Sign up with GitHub
   - Create a new project

2. **Configure Neon:**
   - Project name: `clinical-case-platform`
   - Region: Choose closest to your users (e.g., `Singapore` for Vietnamese users)
   - Compute size: Free tier (0.25 vCPU, 256MB RAM)

3. **Get Connection Details:**
   - From Neon dashboard, find your connection string:

   ```
   postgresql://username:password@ep-cool-name-123456.region.aws.neon.tech/clinical_case_platform
   ```

4. **Update Railway Environment Variables:**
   - `DB_HOST`: Extract from Neon connection string
   - `DB_NAME`: Extract or use default
   - `DB_USER`: Extract
   - `DB_PASSWORD`: Extract

### Step 6.3: Set Up Upstash Redis

1. **Create Upstash Account:**
   - Go to <https://upstash.com>
   - Sign up with GitHub
   - Create a new Redis database

2. **Configure Upstash:**
   - Region: Choose closest to users
   - Tier: Free (10K commands/day)

3. **Get Connection Details:**
   - From Upstash dashboard, copy the Redis URL:

   ```
   redis://default:your-password@your-redis.upstash.io:6379
   ```

### Step 6.4: Deploy to Railway

1. **Create Railway Account:**
   - Go to <https://railway.app>
   - Sign up with GitHub

2. **Create New Project:**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will detect it's a Python/Django app

3. **Configure Build Command:**
   Railway should auto-detect, but verify:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn clinical_case_platform.asgi:application --worker-class aiohttp.GunicornWebWorker --bind 0.0.0.0:$PORT`

4. **Add Environment Variables:**
   - Go to Railway dashboard → your project → Variables
   - Add all variables from `.env.production`

5. **Set Start Command:**
   - Navigate to Settings → Start Command
   - Use: `gunicorn clinical_case_platform.asgi:application --worker-class aiohttp.GunicornWebWorker --bind 0.0.0.0:$PORT`

   **Note**: For WebSocket support, use Daphne instead:

   ```
   daphne -b 0.0.0.0 -p $PORT clinical_case_platform.asgi:application
   ```

6. **Deploy:**
   - Railway will automatically deploy
   - Monitor logs for any errors

### Step 6.5: Configure Domain (Optional)

1. In Railway dashboard, go to Settings → Networking
2. Add custom domain if you have one
3. Update `ALLOWED_HOSTS` accordingly

### Step 6.6: Run Migrations

1. **Use Railway CLI:**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
cd clinical-case-platform/backend
railway link

# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser

# Rebuild search index
railway run python manage.py rebuild_case_search

# Seed case choices
railway run python manage.py seed_case_choices
```

### Step 6.7: Verify Deployment

1. Check health endpoint: `https://your-app.railway.app/api/health/`
2. Check API docs: `https://your-app.railway.app/api/docs/`
3. Test authentication
4. Verify database connections

---

## 7. Step-by-Step Deployment: Render

### Step 7.1: Create Render Account

- Sign up at <https://render.com>
- Connect GitHub repository

### Step 7.2: Create PostgreSQL Database

1. **Dashboard → New → PostgreSQL**
2. Configure:
   - Name: `clinical-case-db`
   - Region: Singapore
   - Plan: Free (Free tier includes 1 database)
3. Note the `Internal Database URL`

### Step 7.3: Create Web Service

1. **Dashboard → New → Web Service**
2. Configure:
   - Name: `clinical-case-api`
   - Region: Singapore
   - Branch: `main`
   - Root Directory: `backend`

3. **Environment Settings:**
   - Runtime: `Python 3.12`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn clinical_case_platform.asgi:application --worker-class aiohttp.GunicornWebWorker --bind 0.0.0.0:$PORT`

4. **Environment Variables:**

   ```bash
   # Add from Render PostgreSQL
   DATABASE_URL=<your-postgres-internal-url>

   # Add these manually
   DEBUG=False
   SECRET_KEY=<your-secret-key>
   ALLOWED_HOSTS=<your-render-domain>.onrender.com
   CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app

   # Redis (use Upstash or Render Redis)
   REDIS_URL=<your-redis-url>
   CELERY_BROKER_URL=<your-redis-url>
   CELERY_RESULT_BACKEND=<your-redis-url>

   FRONTEND_URL=https://your-frontend.vercel.app
   ```

### Step 7.4: Configure Health Check

1. **Health Check Path:** `/api/health/`
2. Render will ping this endpoint to verify the service is running

### Step 7.5: Add Redis (if using Render Redis)

1. **Dashboard → New → Redis**
2. Note the Redis connection URL
3. Add to Web Service environment variables

### Step 7.6: Run Initial Setup

Use Render Shell or connect via SSH:

```bash
# Connect to shell
renderctl ssh connect <service-id>

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Rebuild search
python manage.py rebuild_case_search
python manage.py seed_case_choices
```

---

## 8. Step-by-Step Deployment: Fly.io

### Step 8.1: Install Fly CLI

```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

### Step 8.2: Authenticate

```bash
fly auth login
```

### Step 8.3: Launch Application

```bash
cd backend

# Create fly.toml
fly launch

# Configure:
# - App name: clinical-case-api
# - Region: sin (Singapore)
# - Would you like to set up a Postgres database now? No
# - Would you like to set up an Upstash Redis database now? No
```

### Step 8.4: Create Fly App Manually

```bash
fly apps create clinical-case-api
```

### Step 8.5: Configure fly.toml

Create/update `backend/fly.toml`:

```toml
app = "clinical-case-api"
primary_region = "sin"
kill_signal = "SIGINT"
kill_timeout = "5s"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8080"
  PYTHONUNBUFFERED = "1"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[vm]]
  memory = "512mb"
  cpu_kind = "shared"
  cpus = 1
```

### Step 8.6: Create Dockerfile (if not exists)

The backend already has a Dockerfile. Ensure it uses:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# ... existing Dockerfile content ...

# Expose port
EXPOSE 8080

# Use daphne for ASGI/WebSocket
CMD ["daphne", "-b", "0.0.0.0", "-p", "8080", "clinical_case_platform.asgi:application"]
```

### Step 8.7: Set Secrets

```bash
# Django secrets
fly secrets set SECRET_KEY=your-production-secret-key

# Database
fly secrets set DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Redis
fly secrets set REDIS_URL=redis://host:6379

# Other required vars
fly secrets set DEBUG=False
fly secrets set ALLOWED_HOSTS=clinical-case-api.fly.dev
fly secrets set CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

### Step 8.8: Deploy

```bash
fly deploy

# Check status
fly status

# View logs
fly logs
```

### Step 8.9: Run Migrations

```bash
fly ssh console

# Inside console
python manage.py migrate
python manage.py createsuperuser
python manage.py rebuild_case_search
python manage.py seed_case_choices
exit
```

### Step 8.10: Scale Down (Free Tier)

```bash
# Set to sleep when not in use
fly scale count 0

# Or set autoscaling
fly scale auto
```

---

## 9. Step-by-Step Deployment: Google Cloud Run

### Step 9.1: Prerequisites

```bash
# Install Google Cloud SDK
brew install google-cloud-sdk  # macOS
# or download from https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set project
gcloud config set project your-project-id

# Enable required APIs
gcloud services enable run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com
```

### Step 9.2: Create Artifact Registry

```bash
# Create repository
gcloud artifacts repositories create clinical-case-platform \
  --repository-format=docker \
  --location=asia-southeast1

# Configure Docker auth
gcloud auth configure-docker asia-southeast1-docker.pkg.dev
```

### Step 9.3: Build and Push Docker Image

```bash
cd backend

# Build image
gcloud builds submit --tag asia-southeast1-docker.pkg.dev/your-project-id/clinical-case-platform/backend:latest

# Alternative: Build locally with Docker
docker build -t asia-southeast1-docker.pkg.dev/your-project-id/clinical-case-platform/backend:latest .
docker push asia-southeast1-docker.pkg.dev/your-project-id/clinical-case-platform/backend:latest
```

### Step 9.4: Create Cloud SQL Instance

1. **Via Console:**
   - Go to Cloud SQL → Create Instance → PostgreSQL
   - Configuration:
     - Instance ID: `clinical-case-db`
     - Region: asia-southeast1 (Singapore)
     - Zone: any
     - Machine type: Small (1 vCPU, 1.7GB) - free tier eligible

2. **Via CLI:**

```bash
gcloud sql instances create clinical-case-db \
  --database-version=POSTGRES_16 \
  --tier=db-f1-micro \
  --region=asia-southeast1 \
  --storage-type=SSD \
  --storage-size=10GB
```

### Step 9.5: Create Database and User

```bash
# Create database
gcloud sql databases create clinical_case_platform --instance=clinical-case-db

# Create user
gcloud sql users create postgres \
  --instance=clinical-case-db \
  --password=your-password
```

### Step 9.6: Create Secret Manager Secrets

```bash
# Create secrets
echo -n "your-production-secret-key" | gcloud secrets create SECRET_KEY --data-file=-

# Grant access to Cloud Run service
gcloud projects add-iam-policy-binding your-project-id \
  --member="serviceAccount:your-project-id@appspot.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### Step 9.7: Deploy to Cloud Run

```bash
# Get connection name
CLOUD_SQL_CONNECTION=$(gcloud sql instances describe clinical-case-db \
  --format="value(connectionName)")

# Deploy
gcloud run deploy clinical-case-api \
  --image=asia-southeast1-docker.pkg.dev/your-project-id/clinical-case-platform/backend:latest \
  --platform=managed \
  --region=asia-southeast1 \
  --allow-unauthenticated \
  --port=8080 \
  --memory=512Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=10 \
  --concurrency=80 \
  --timeout=300 \
  --set-env-vars="DEBUG=False" \
  --set-env-vars="ALLOWED_HOSTS=your-service-run.app" \
  --set-env-vars="CLOUD_SQL_CONNECTION_NAME=${CLOUD_SQL_CONNECTION}" \
  --add-cloudsql-instances=clinical-case-db \
  --service-account=your-sa@your-project-id.iam.gserviceaccount.com
```

### Step 9.8: Set Environment Variables

```bash
# Update service with all env vars
gcloud run services update clinical-case-api \
  --region=asia-southeast1 \
  --set-env-vars="DEBUG=False" \
  --set-env-vars="SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)" \
  --set-env-vars="ALLOWED_HOSTS=clinical-case-api-*.run.app" \
  --set-env-vars="DATABASE_URL=postgresql://postgres:password@/clinical_case_platform?host=/cloudsql/your-project:asia-southeast1:clinical-case-db" \
  --set-env-vars="REDIS_URL=redis://your-redis-host:6379"
```

### Step 9.9: Run Migrations

```bash
# Create job for migrations
gcloud run jobs create run-migrations \
  --image=asia-southeast1-docker.pkg.dev/your-project-id/clinical-case-platform/backend:latest \
  --command="/bin/sh" \
  --args="-c,python manage.py migrate && python manage.py createsuperuser"

# Execute job
gcloud run jobs run run-migrations
```

---

## 10. Frontend Deployment (Vercel/Netlify)

### Option A: Vercel (Recommended)

#### Step 10A.1: Prepare Frontend

1. **Create `frontend/vercel.json`:**

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-backend.railway.app/api/:path*"
    },
    {
      "source": "/media/:path*",
      "destination": "https://your-backend.railway.app/media/:path*"
    },
    {
      "source": "/ws/notifications/:path*",
      "destination": "wss://your-backend.railway.app/ws/notifications/:path*"
    }
  ],
  "env": {
    "VITE_API_BASE_URL": "https://your-backend.railway.app/api",
    "VITE_WS_URL": "wss://your-backend.railway.app"
  }
}
```

1. **Update API service in `frontend/src/services/api.ts`:**

```typescript
const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_BASE_URL || "https://your-backend.railway.app/api",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});
```

#### Step 10A.2: Deploy to Vercel

1. **Connect Repository:**
   - Go to <https://vercel.com>
   - Sign up with GitHub
   - Click "New Project"
   - Import your repository
   - Set root directory to `frontend`

2. **Configure Build Settings:**
   - Framework Preset: `Vite`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

3. **Add Environment Variables:**

   ```
   VITE_API_BASE_URL=https://your-backend.railway.app/api
   VITE_WS_URL=wss://your-backend.railway.app
   ```

4. **Deploy:**
   - Click "Deploy"
   - Vercel will automatically build and deploy

#### Step 10A.3: Configure Custom Domain (Optional)

1. In Vercel dashboard → Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Update CORS settings in backend

### Option B: Netlify

#### Step 10B.1: Create netlify.toml

```toml
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "20"

[[redirects]]
  from = "/api/*"
  to = "https://your-backend.railway.app/api/*"
  status = 200
  force = true

[[redirects]]
  from = "/media/*"
  to = "https://your-backend.railway.app/media/*"
  status = 200
  force = true

[[redirects]]
  from = "/ws/*"
  to = "wss://your-backend.railway.app/ws/*"
  status = 200
  force = true

[context.production.environment]
  VITE_API_BASE_URL = "https://your-backend.railway.app/api"
```

#### Step 10B.2: Deploy to Netlify

1. Connect GitHub repository
2. Configure build settings
3. Add environment variables
4. Deploy

### Step 10.3: Update Backend CORS

After deploying frontend, update backend CORS settings:

```bash
# In Railway/Render/Fly dashboard
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.netlify.app
```

---

## 11. Client Handoff Guide

### 11.1: Documentation Package

Prepare a comprehensive documentation package for the client IT team:

#### Contents

1. **System Overview Document** (this guide)
2. **Architecture Diagram** (provide `docs/hmsERDnminh.png`)
3. **API Documentation** (deployed Swagger UI)
4. **User Manual** (end-user guides)
5. **Troubleshooting Guide** (common issues)
6. **Support Contacts**

### 11.2: Environment Configuration Guide

Provide the client with:

#### Required Environment Variables

```bash
# Django Core
DEBUG=False
SECRET_KEY=<generate-secure-50-char-key>
ALLOWED_HOSTS=<domain1.com>,<domain2.com>

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname
# OR individual:
DB_ENGINE=django.db.backends.postgresql
DB_NAME=clinical_case_platform
DB_USER=postgres
DB_PASSWORD=<db-password>
DB_HOST=<db-host>
DB_PORT=5432

# Redis
REDIS_URL=redis://host:6379/0
CELERY_BROKER_URL=redis://host:6379/0
CELERY_RESULT_BACKEND=redis://host:6379/0

# CORS
CORS_ALLOWED_ORIGINS=<frontend-domain>

# Email (for password reset)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=<email>@gmail.com
EMAIL_HOST_PASSWORD=<app-password>

# Frontend URL
FRONTEND_URL=<frontend-url>

# AI Features (optional)
ASR_ENABLED=false  # or true if using
OCR_ENGINE=DOCTR
```

### 11.3: Infrastructure Recommendations

For production (non-free tier):

| Component    | Recommended Service      | Reason                |
| ------------ | ------------------------ | --------------------- |
| Backend Host | Railway/Render/Cloud Run | Managed, auto-scaling |
| Database     | Neon/Supabase/AWS RDS    | Managed PostgreSQL    |
| Redis        | Upstash/Redis Cloud      | Serverless Redis      |
| Frontend     | Vercel/Netlify           | CDN, edge caching     |
| Storage      | AWS S3/Cloud Storage     | Media file storage    |
| CDN          | Cloudflare               | Security, caching     |
| Monitoring   | Sentry/DataDog           | Error tracking        |
| CI/CD        | GitHub Actions           | Automated deployments |

### 11.4: Deployment Checklist for Client IT

```markdown
## Production Deployment Checklist

### Pre-Deployment

- [ ] Obtain domain names for frontend and backend
- [ ] Set up SSL certificates (usually automatic with platforms)
- [ ] Configure DNS records
- [ ] Set up monitoring and alerting
- [ ] Create backup strategy
- [ ] Document incident response plan

### Database Setup

- [ ] Create PostgreSQL database
- [ ] Configure connection pooling
- [ ] Enable automated backups
- [ ] Set up read replicas (if needed)
- [ ] Test database connectivity

### Backend Deployment

- [ ] Clone repository to deployment environment
- [ ] Configure environment variables (SECRET_KEY, DB, Redis)
- [ ] Run database migrations
- [ ] Create admin superuser
- [ ] Rebuild search index
- [ ] Seed case choices
- [ ] Test health endpoint
- [ ] Verify API documentation

### Redis Setup

- [ ] Create Redis instance
- [ ] Configure connection
- [ ] Test Redis connectivity
- [ ] Verify Celery worker connection

### Frontend Deployment

- [ ] Configure API base URL
- [ ] Configure WebSocket URL
- [ ] Build frontend
- [ ] Deploy to hosting
- [ ] Verify static assets
- [ ] Test authentication flow

### Integration Testing

- [ ] Test user registration
- [ ] Test user login
- [ ] Test case creation
- [ ] Test file uploads
- [ ] Test case sharing
- [ ] Test real-time notifications
- [ ] Test export functionality

### Security Hardening

- [ ] Enable HTTPS everywhere
- [ ] Configure CSP headers
- [ ] Set up rate limiting
- [ ] Enable audit logging
- [ ] Configure backup retention
- [ ] Review CORS settings

### Post-Deployment

- [ ] Monitor error rates
- [ ] Set up performance monitoring
- [ ] Document support contacts
- [ ] Train end users
- [ ] Provide IT team documentation
```

### 11.5: IT Team Training Outline

#### Module 1: System Overview (1 hour)

- Architecture explanation
- Technology stack overview
- User roles and permissions

#### Module 2: Server Management (2 hours)

- Accessing deployment dashboard
- Viewing logs
- Restarting services
- Environment variable management
- Database backups

#### Module 3: Monitoring & Troubleshooting (1 hour)

- Health check endpoints
- Common error scenarios
- Log analysis
- When to escalate

#### Module 4: User Management (1 hour)

- Admin panel overview
- Creating users
- Managing roles
- Resetting passwords

---

## 12. Environment Configuration Reference

### Full Environment Variables List

```bash
# ===========================================
# DJANGO CORE
# ===========================================
DEBUG=False
SECRET_KEY=<50+ character random string>
ALLOWED_HOSTS=api.example.com,localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=clinical_case_platform.settings_production

# ===========================================
# DATABASE
# ===========================================
# Option 1: DATABASE_URL (recommended)
DATABASE_URL=postgresql://user:password@host:5432/clinical_case_platform

# Option 2: Individual settings
DB_ENGINE=django.db.backends.postgresql
DB_NAME=clinical_case_platform
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=host
DB_PORT=5432

# ===========================================
# REDIS
# ===========================================
REDIS_URL=redis://default:password@host:6379
CELERY_BROKER_URL=redis://default:password@host:6379
CELERY_RESULT_BACKEND=redis://default:password@host:6379

# ===========================================
# CORS
# ===========================================
CORS_ALLOWED_ORIGINS=https://frontend.example.com,http://localhost:5173

# ===========================================
# EMAIL
# ===========================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Clinical Case Platform <noreply@example.com>

# ===========================================
# FRONTEND
# ===========================================
FRONTEND_URL=https://frontend.example.com

# ===========================================
# AI FEATURES (Optional)
# ===========================================
ASR_ENABLED=false
OCR_ENGINE=DOCTR
TRANSFORMERS_CACHE=/app/ai/asr/phowhisper
HF_HOME=/app/ai/asr/phowhisper

# ===========================================
# STORAGE (for S3 - optional)
# ===========================================
USE_S3=TRUE
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=ap-southeast-1

# ===========================================
# SECURITY
# ===========================================
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
CSRF_TRUSTED_ORIGINS=https://frontend.example.com
```

### Generating a Secure SECRET_KEY

```bash
# Python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Node.js
node -e "console.log(require('crypto').randomBytes(50).toString('hex'))"

# OpenSSL
openssl rand -base64 50
```

---

## 13. Troubleshooting

### Common Issues and Solutions

#### Issue: 500 Internal Server Error

**Symptoms:**

- Backend returns 500 errors
- No specific error message shown

**Diagnosis:**

```bash
# Check logs
railway logs
# or
fly logs
# or
render logs

# Common causes:
# 1. Missing environment variables
# 2. Database connection failed
# 3. Redis connection failed
# 4. Migration not run
```

**Solutions:**

1. Verify all environment variables are set
2. Check database connectivity
3. Run pending migrations
4. Check for syntax errors in code

#### Issue: CORS Errors

**Symptoms:**

- Browser console shows CORS policy errors
- API calls fail from frontend

**Solution:**

```bash
# Update CORS_ALLOWED_ORIGINS
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://www.your-domain.com
```

#### Issue: Database Connection Failed

**Symptoms:**

- `could not connect to server`
- `connection refused`

**Solutions:**

1. Verify database is running
2. Check connection string format
3. Verify IP whitelist (if applicable)
4. Check connection pooling settings

#### Issue: WebSocket Connection Failed

**Symptoms:**

- Notifications not working
- Real-time features unresponsive

**Solutions:**

1. Ensure using `wss://` not `ws://` for HTTPS sites
2. Check `ALLOWED_HOSTS` includes frontend domain
3. Verify Redis is accessible
4. Check WebSocket proxy settings

#### Issue: File Uploads Fail

**Symptoms:**

- Upload returns 413 or timeout
- Files not saved

**Solutions:**

1. Increase request timeout
2. Check disk space
3. Verify media directory permissions
4. Configure proxy body size limits

#### Issue: Celery Tasks Not Running

**Symptoms:**

- Background tasks not executing
- Export generation fails

**Solutions:**

1. Verify Redis is running
2. Check Celery worker logs
3. Ensure `CELERY_BROKER_URL` is correct
4. Restart Celery worker

### Health Check Endpoints

```bash
# Backend health
curl https://api.example.com/api/health/

# Expected response:
{
  "status": "healthy",
  "service": "Clinical Case Platform API",
  "version": "1.0.0",
  "database": "connected"
}
```

### Log Locations

| Platform  | Log Access                                       |
| --------- | ------------------------------------------------ |
| Railway   | `railway logs` or Dashboard → Deployments → Logs |
| Render    | Dashboard → Services → Logs                      |
| Fly.io    | `fly logs`                                       |
| Cloud Run | `gcloud run logs read clinical-case-api`         |

---

## 14. Maintenance

### Regular Maintenance Tasks

#### Daily

- Monitor error rates
- Check health endpoints
- Review failed job alerts

#### Weekly

- Review application logs
- Check database performance
- Verify backups completed

#### Monthly

- Apply security patches
- Review and rotate logs
- Update dependencies
- Performance optimization review

### Backup Strategy

#### Database Backups

```bash
# PostgreSQL backup
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME -F c -b -v -f backup.sql

# Automated with Neon
# Neon provides automatic daily backups
# Configure retention period in dashboard
```

#### File Backups

```bash
# Backup media files
tar -czf media_backup.tar.gz /app/media/

# Sync to cloud storage (optional)
aws s3 sync /app/media/ s3://your-bucket/media/
```

### Updating the Application

#### Backend Update Process

```bash
# 1. Pull latest code
git pull origin main

# 2. Install new dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Rebuild search index (if updated)
python manage.py rebuild_case_search

# 5. Restart service
# (Platform-specific)
railway restart
# or
fly deploy
# or
gcloud run deploy ...
```

#### Frontend Update Process

```bash
# 1. Pull latest code
git pull origin main

# 2. Install new dependencies
npm install

# 3. Build
npm run build

# 4. Deploy
# (Vercel auto-deploys on main branch push)
```

### Performance Monitoring

```bash
# Django Debug Toolbar (development only)
# Not for production!

# Use Django Silk for profiling
pip install django-silk
```

### Security Updates

```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update all packages
pip-review --auto  # after pip install pip-review
```

---

## Quick Reference Card

### Essential Commands

```bash
# Local Development
cd backend && pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

cd frontend && npm install
npm run dev

# Docker (if using)
docker-compose up -d
docker-compose logs -f

# Deployment Verification
curl https://api.example.com/api/health/
curl https://api.example.com/api/docs/

# Database Operations
python manage.py migrate
python manage.py createsuperuser
python manage.py rebuild_case_search
python manage.py seed_case_choices

# Celery
celery -A clinical_case_platform worker -l info
celery -A clinical_case_platform beat -l info
```

### Port Reference

| Service     | Local Port | Production |
| ----------- | ---------- | ---------- |
| Backend API | 8000       | 8080/8000  |
| Frontend    | 5173       | 80/443     |
| PostgreSQL  | 5432       | Varies     |
| Redis       | 6379       | Varies     |
| WebSocket   | 8000/ws    | 80/ws      |

---

## Support Resources

### Documentation Links

- Django 5.1: <https://docs.djangoproject.com/en/5.1/>
- DRF: <https://www.django-rest-framework.org/>
- Vue 3: <https://vuejs.org/guide/>
- PrimeVue: <https://primevue.org/>
- Railway: <https://docs.railway.app/>
- Vercel: <https://vercel.com/docs/>

### Troubleshooting Resources

- Django Debug Toolbar: <https://django-debug-toolbar.readthedocs.io/>
- Django Channels: <https://channels.readthedocs.io/>
- Celery: <https://docs.celeryq.dev/>

---

_Document Version: 1.0_
Last Updated: March 2026
_For: Clinical Case Management Platform Deployment_

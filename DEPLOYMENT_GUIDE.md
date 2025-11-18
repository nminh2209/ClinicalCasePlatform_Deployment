# Deployment Guide: Vercel + Render
**Clinical Case Platform - Production Deployment**

## Architecture Overview
- **Frontend**: Vercel (Vue.js static hosting)
- **Backend**: Render (Django API)
- **Database**: Render PostgreSQL (managed)
- **Media Storage**: AWS S3 or Cloudinary (for file uploads)

---

## 📋 Prerequisites

### Required Accounts
1. **Vercel Account** - https://vercel.com/signup (free tier available)
2. **Render Account** - https://render.com/register (free tier available)
3. **GitHub Account** - Repository for code deployment
4. **AWS Account** (optional) - For S3 media storage

### Local Requirements
- Git installed
- Node.js 18+ installed
- Python 3.10+ installed
- PostgreSQL client (optional, for local testing)

---

## 🗄️ Part 1: Database Setup on Render

### Step 1.1: Create PostgreSQL Database

1. **Login to Render Dashboard**
   - Go to https://dashboard.render.com/

2. **Create New PostgreSQL Database**
   - Click **"New +"** → **"PostgreSQL"**
   - Fill in details:
     ```
     Name: clinical-case-db
     Database: clinical_case_platform
     User: clinical_case_user
     Region: Singapore (or closest to your users)
     PostgreSQL Version: 15
     Plan: Free (or Starter $7/month for better performance)
     ```

3. **Save Database Credentials**
   After creation, note these values (found in "Info" tab):
   ```
   Internal Database URL: postgresql://user:pass@hostname:5432/dbname
   External Database URL: postgresql://user:pass@hostname:5432/dbname
   PSQL Command: psql -h hostname -U user dbname
   
   Hostname: dpg-xxxxx-a.singapore-postgres.render.com
   Port: 5432
   Database: clinical_case_platform
   Username: clinical_case_user
   Password: [auto-generated]
   ```

4. **Test Connection** (Optional)
   ```bash
   # Using the PSQL command from Render
   psql -h dpg-xxxxx-a.singapore-postgres.render.com -U clinical_case_user clinical_case_platform
   ```

---

## 🚀 Part 2: Backend Deployment on Render

### Step 2.1: Prepare Backend for Production

1. **Create Production Settings File**
   ```bash
   cd backend
   ```

Create `backend/clinical_case_platform/settings_production.py`:

```python
from .settings import *
import os
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'clinical-case-api.onrender.com',  # Your Render backend URL
    'localhost',
    '127.0.0.1',
]

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    'https://your-app.vercel.app',  # Your Vercel frontend URL
    'http://localhost:5173',  # Local development
]

CORS_ALLOW_CREDENTIALS = True

# Database Configuration
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static Files (WhiteNoise)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media Files (Use S3 or Cloudinary in production)
if os.environ.get('USE_S3') == 'TRUE':
    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'ap-southeast-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
else:
    # Fallback to local storage (not recommended for production)
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    'https://clinical-case-api.onrender.com',
    'https://your-app.vercel.app',
]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

2. **Update requirements.txt**
   
   Add production dependencies:
   ```bash
   cd backend
   ```

Check if these are in `requirements.txt`, if not add them:
```txt
# Production Dependencies
gunicorn==21.2.0
whitenoise==6.6.0
dj-database-url==2.1.0
psycopg2-binary==2.9.9

# Optional: For AWS S3 media storage
boto3==1.34.0
django-storages==1.14.2
```

3. **Create `build.sh` Script**

Create `backend/build.sh`:
```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
```

Make it executable:
```bash
chmod +x build.sh
```

4. **Create `render.yaml` Configuration**

Create `backend/render.yaml`:
```yaml
services:
  - type: web
    name: clinical-case-api
    runtime: python
    buildCommand: "./build.sh"
    startCommand: "gunicorn clinical_case_platform.wsgi:application"
    envVars:
      - key: DJANGO_SETTINGS_MODULE
        value: clinical_case_platform.settings_production
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: clinical-case-db
          property: connectionString
      - key: DEBUG
        value: False
      - key: USE_S3
        value: FALSE
```

### Step 2.2: Deploy Backend to Render

1. **Push Code to GitHub**
   ```bash
   cd d:\Download\randoms\HN2.1ProjectA-develop\HN2.1ProjectA-develop
   git add .
   git commit -m "Prepare for production deployment"
   git push origin main
   ```

2. **Create Web Service on Render**
   - Go to https://dashboard.render.com/
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub repository
   - Configure:
     ```
     Name: clinical-case-api
     Region: Singapore (match your database)
     Branch: main
     Root Directory: backend
     Runtime: Python 3
     Build Command: ./build.sh
     Start Command: gunicorn clinical_case_platform.wsgi:application
     Plan: Free (or Starter for always-on)
     ```

3. **Set Environment Variables**
   In Render dashboard → Your Web Service → "Environment":
   ```
   DJANGO_SETTINGS_MODULE=clinical_case_platform.settings_production
   SECRET_KEY=[auto-generated or use Django secret key generator]
   DATABASE_URL=[Link to your Render PostgreSQL]
   DEBUG=False
   PYTHON_VERSION=3.11.0
   ALLOWED_HOSTS=clinical-case-api.onrender.com
   ```

4. **Deploy**
   - Click **"Create Web Service"**
   - Wait for build to complete (~5-10 minutes)
   - Check logs for errors

5. **Verify Deployment**
   ```bash
   # Test API endpoint
   curl https://clinical-case-api.onrender.com/api/health/
   ```

### Step 2.3: Run Initial Migrations

1. **Connect to Render Shell**
   - In Render dashboard → Your Web Service → "Shell"
   - Or use Render CLI:
   ```bash
   render shell clinical-case-api
   ```

2. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

3. **Populate Initial Data** (Optional)
   ```bash
   python manage.py populate_medical_terms
   ```

---

## 🎨 Part 3: Frontend Deployment on Vercel

### Step 3.1: Prepare Frontend for Production

1. **Update Environment Variables**

Create `frontend/.env.production`:
```env
VITE_API_URL=https://clinical-case-api.onrender.com
VITE_APP_NAME=Clinical Case Platform
VITE_APP_ENV=production
```

2. **Update API Base URL**

Verify `frontend/src/services/api.ts` uses environment variable:
```typescript
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

3. **Build Test Locally**
   ```bash
   cd frontend
   npm install
   npm run build
   ```
   
   Check for errors. The `dist/` folder should be created.

### Step 3.2: Deploy to Vercel

#### Method 1: Using Vercel Dashboard (Recommended)

1. **Login to Vercel**
   - Go to https://vercel.com/login
   - Sign in with GitHub

2. **Import Project**
   - Click **"Add New"** → **"Project"**
   - Import your GitHub repository
   - Select the repository

3. **Configure Project**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

4. **Set Environment Variables**
   - Click **"Environment Variables"**
   - Add:
     ```
     VITE_API_URL=https://clinical-case-api.onrender.com
     VITE_APP_NAME=Clinical Case Platform
     VITE_APP_ENV=production
     ```

5. **Deploy**
   - Click **"Deploy"**
   - Wait for deployment (~2-3 minutes)
   - Your app will be available at `https://your-app.vercel.app`

#### Method 2: Using Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   cd frontend
   vercel --prod
   ```

4. **Set Environment Variables**
   ```bash
   vercel env add VITE_API_URL production
   # Enter: https://clinical-case-api.onrender.com
   
   vercel env add VITE_APP_NAME production
   # Enter: Clinical Case Platform
   ```

5. **Redeploy with Environment Variables**
   ```bash
   vercel --prod
   ```

### Step 3.3: Configure Custom Domain (Optional)

1. **In Vercel Dashboard**
   - Go to your project → "Settings" → "Domains"
   - Add your custom domain (e.g., `clinical-cases.yourdomain.com`)
   - Follow DNS configuration instructions

2. **Update Backend CORS Settings**
   Update `backend/clinical_case_platform/settings_production.py`:
   ```python
   CORS_ALLOWED_ORIGINS = [
       'https://your-app.vercel.app',
       'https://clinical-cases.yourdomain.com',  # Add custom domain
   ]
   
   CSRF_TRUSTED_ORIGINS = [
       'https://clinical-case-api.onrender.com',
       'https://your-app.vercel.app',
       'https://clinical-cases.yourdomain.com',  # Add custom domain
   ]
   ```

3. **Redeploy Backend**
   - Push changes to GitHub
   - Render will auto-deploy

---

## 🔒 Part 4: Security & Environment Variables

### Step 4.1: Generate Secure SECRET_KEY

```python
# Run this locally
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Add to Render environment variables.

### Step 4.2: Update ALLOWED_HOSTS

In Render dashboard, set:
```
ALLOWED_HOSTS=clinical-case-api.onrender.com,your-custom-domain.com
```

### Step 4.3: Complete Environment Variables List

**Backend (Render):**
```env
# Django
DJANGO_SETTINGS_MODULE=clinical_case_platform.settings_production
SECRET_KEY=[your-generated-secret-key]
DEBUG=False
ALLOWED_HOSTS=clinical-case-api.onrender.com

# Database (auto-linked from Render PostgreSQL)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# CORS
CORS_ALLOWED_ORIGINS=https://your-app.vercel.app

# Media Storage (if using S3)
USE_S3=TRUE
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=ap-southeast-1

# Email (if using SendGrid/AWS SES)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

**Frontend (Vercel):**
```env
VITE_API_URL=https://clinical-case-api.onrender.com
VITE_APP_NAME=Clinical Case Platform
VITE_APP_ENV=production
```

---

## 📦 Part 5: Media Storage Setup (AWS S3)

### Step 5.1: Create S3 Bucket

1. **Login to AWS Console**
   - Go to https://console.aws.amazon.com/s3/

2. **Create Bucket**
   ```
   Bucket name: clinical-case-media
   Region: Asia Pacific (Singapore) ap-southeast-1
   Block all public access: OFF (we'll use signed URLs)
   Bucket Versioning: Disabled
   ```

3. **Configure CORS**
   - Go to bucket → "Permissions" → "CORS"
   - Add:
   ```json
   [
     {
       "AllowedHeaders": ["*"],
       "AllowedMethods": ["GET", "PUT", "POST", "DELETE", "HEAD"],
       "AllowedOrigins": [
         "https://your-app.vercel.app",
         "https://clinical-case-api.onrender.com"
       ],
       "ExposeHeaders": ["ETag"]
     }
   ]
   ```

4. **Create IAM User**
   - Go to IAM → "Users" → "Create user"
   - User name: `clinical-case-s3-user`
   - Attach policy: `AmazonS3FullAccess` (or create custom policy)
   - Create access key → Save credentials

5. **Add S3 Credentials to Render**
   ```env
   USE_S3=TRUE
   AWS_ACCESS_KEY_ID=AKIAXXXXXXXXX
   AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxx
   AWS_STORAGE_BUCKET_NAME=clinical-case-media
   AWS_S3_REGION_NAME=ap-southeast-1
   ```

### Step 5.2: Update Django Settings for S3

In `settings_production.py`, ensure:
```python
if os.environ.get('USE_S3') == 'TRUE':
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
```

---

## 🔍 Part 6: Testing & Verification

### Step 6.1: Health Check Endpoints

Add health check to `backend/clinical_case_platform/urls.py`:
```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'database': 'connected',
        'version': '1.0.0'
    })

urlpatterns = [
    path('api/health/', health_check),
    # ... other paths
]
```

### Step 6.2: Test Checklist

- [ ] **Backend API**: `curl https://clinical-case-api.onrender.com/api/health/`
- [ ] **Frontend loads**: Visit `https://your-app.vercel.app`
- [ ] **Login works**: Test with superuser credentials
- [ ] **Database connection**: Create a test case
- [ ] **File upload**: Upload an attachment (if S3 configured)
- [ ] **CORS works**: No console errors on frontend
- [ ] **Social feed**: Publish a case to feed
- [ ] **Comments work**: Add comment on feed
- [ ] **Reactions work**: Test all 4 reaction types

### Step 6.3: Performance Testing

```bash
# Test API response time
curl -w "@curl-format.txt" -o /dev/null -s https://clinical-case-api.onrender.com/api/cases/

# curl-format.txt:
time_namelookup:  %{time_namelookup}\n
time_connect:  %{time_connect}\n
time_starttransfer:  %{time_starttransfer}\n
time_total:  %{time_total}\n
```

---

## 🔧 Part 7: Troubleshooting

### Common Issues

#### Issue 1: "DisallowedHost at /"
**Solution:** Add your Render URL to `ALLOWED_HOSTS` in environment variables

#### Issue 2: "CORS policy: No 'Access-Control-Allow-Origin' header"
**Solution:** 
1. Check `CORS_ALLOWED_ORIGINS` includes Vercel URL
2. Verify `django-cors-headers` is installed
3. Check middleware order in settings

#### Issue 3: Database connection timeout
**Solution:**
1. Verify `DATABASE_URL` environment variable
2. Check database is in same region as web service
3. Ensure PostgreSQL is running (Render dashboard)

#### Issue 4: Static files not loading
**Solution:**
1. Run `python manage.py collectstatic` in Render shell
2. Verify `STATIC_ROOT` in settings
3. Check WhiteNoise middleware is configured

#### Issue 5: 502 Bad Gateway on Render
**Solution:**
1. Check Render logs for Python errors
2. Verify `gunicorn` is in requirements.txt
3. Check `Procfile` or start command is correct

#### Issue 6: Vercel build fails
**Solution:**
1. Check `package.json` has correct build script
2. Verify Node version compatibility
3. Check for TypeScript errors: `npm run build` locally

### Viewing Logs

**Render Backend Logs:**
```bash
# In Render dashboard
Your Service → Logs (live tail)

# Or use CLI
render logs clinical-case-api
```

**Vercel Frontend Logs:**
```bash
# In Vercel dashboard
Your Project → Deployments → [Latest] → View Function Logs

# Or use CLI
vercel logs your-app.vercel.app
```

---

## 📊 Part 8: Monitoring & Maintenance

### Step 8.1: Set Up Monitoring

**Backend (Render):**
- Enable "Health Check Path": `/api/health/`
- Set up alerts in Render dashboard

**Frontend (Vercel):**
- Vercel automatically monitors deployments
- Check Analytics for traffic patterns

### Step 8.2: Database Backups

**Render PostgreSQL:**
- Automatic daily backups on paid plans
- Manual backup:
  ```bash
  # From Render dashboard
  Database → Backups → Create Backup
  ```

**Alternative: Manual pg_dump**
```bash
pg_dump -h dpg-xxxxx.singapore-postgres.render.com \
  -U clinical_case_user \
  -d clinical_case_platform \
  -F c -f backup.dump
```

### Step 8.3: Update Strategy

**Backend Updates:**
1. Test changes locally
2. Push to GitHub
3. Render auto-deploys from `main` branch
4. Monitor logs for errors
5. Rollback if needed (Render dashboard → Deploys → Rollback)

**Frontend Updates:**
1. Test changes locally: `npm run build`
2. Push to GitHub
3. Vercel auto-deploys
4. Preview deployments for PR branches
5. Instant rollback available

---

## 💰 Cost Estimate

### Free Tier (Total: $0/month)
- **Vercel**: Unlimited static hosting
- **Render**: 
  - PostgreSQL: Free (expires after 90 days)
  - Web Service: Free (spins down after inactivity)
- **Limitations**: 
  - Backend spins down after 15 min inactivity (cold start ~30s)
  - Database limited to 1GB storage
  - No custom domains on free tier

### Starter Tier (Total: ~$14/month)
- **Vercel**: $0 (hobby plan sufficient)
- **Render**:
  - PostgreSQL Starter: $7/month (10GB storage, always-on)
  - Web Service Starter: $7/month (always-on, no cold starts)
- **Benefits**:
  - No cold starts
  - Better performance
  - 10GB database storage
  - Daily backups

### Production Tier (Total: ~$50-100/month)
- **Vercel Pro**: $20/month (team features, analytics)
- **Render**:
  - PostgreSQL Pro: $20/month (256GB storage, high availability)
  - Web Service Pro: $25/month (2GB RAM, autoscaling)
- **AWS S3**: ~$5-10/month (storage + bandwidth)
- **CloudFlare CDN**: $0 (free tier)

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] Code pushed to GitHub
- [ ] Environment variables documented
- [ ] Database migrations tested locally
- [ ] Build succeeds locally (`npm run build`)
- [ ] All tests passing
- [ ] Security settings configured

### Database Setup
- [ ] Render PostgreSQL created
- [ ] Database credentials saved
- [ ] Connection tested

### Backend Deployment
- [ ] Render web service created
- [ ] Environment variables configured
- [ ] Build script working
- [ ] Migrations run successfully
- [ ] Superuser created
- [ ] Health endpoint responding

### Frontend Deployment
- [ ] Vercel project created
- [ ] Environment variables set
- [ ] Build successful
- [ ] API connection working
- [ ] Routes working correctly

### Post-Deployment
- [ ] All features tested
- [ ] CORS configured correctly
- [ ] File uploads working (if applicable)
- [ ] Performance acceptable
- [ ] Monitoring configured
- [ ] Backup strategy in place

---

## 🆘 Support Resources

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/5.0/howto/deployment/
- **Render Community**: https://community.render.com/
- **Vercel Community**: https://github.com/vercel/vercel/discussions

---

## 🎯 Next Steps After Deployment

1. **Set up custom domain** (optional)
2. **Configure email service** (SendGrid/AWS SES)
3. **Add error tracking** (Sentry)
4. **Set up CDN** (CloudFlare)
5. **Configure monitoring** (UptimeRobot)
6. **Add analytics** (Google Analytics/Plausible)
7. **Set up CI/CD** (GitHub Actions)
8. **Create staging environment**

---

**Deployment Date**: [To be filled]  
**Production URLs**: 
- Frontend: https://your-app.vercel.app  
- Backend: https://clinical-case-api.onrender.com  
- Database: Render PostgreSQL (internal)

**Deployment Status**: ⏳ Pending / ✅ Live / ❌ Failed

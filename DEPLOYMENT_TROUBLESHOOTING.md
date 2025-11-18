# Deployment Troubleshooting Guide

## 🔴 Common Deployment Issues & Solutions

---

## Backend Issues (Render)

### 1. Build Failed

#### Error: `Permission denied: ./build.sh`
**Cause**: Build script doesn't have execute permissions

**Solution**:
```bash
# On your local machine
cd backend
git add build.sh --chmod=+x
git commit -m "Make build.sh executable"
git push

# Or add to build command in Render:
chmod +x build.sh && ./build.sh
```

#### Error: `ModuleNotFoundError: No module named 'xxx'`
**Cause**: Missing package in requirements.txt

**Solution**:
1. Add package to `backend/requirements.txt`
2. Push to GitHub
3. Render will auto-redeploy

#### Error: `ERROR: Could not build wheels for psycopg2`
**Cause**: Wrong PostgreSQL driver

**Solution**:
- Use `psycopg2-binary` instead of `psycopg2` in requirements.txt
- Already fixed in this project ✅

---

### 2. Application Errors

#### Error: `DisallowedHost at /`
**Full error**: "Invalid HTTP_HOST header: 'clinical-case-api.onrender.com'"

**Solution**:
1. Go to Render Dashboard → Your Service → Environment
2. Add/update:
   ```
   ALLOWED_HOSTS=clinical-case-api.onrender.com,localhost
   ```
3. Save (auto-redeploys)

#### Error: `ImproperlyConfigured: settings.DATABASES is improperly configured`
**Cause**: DATABASE_URL not set or incorrect

**Solution**:
1. Go to Render Dashboard → Your Service → Environment
2. Check `DATABASE_URL` exists
3. If missing, link to PostgreSQL database:
   - Click "Add Environment Variable"
   - Name: `DATABASE_URL`
   - Value: Select "Link to database" → Choose your PostgreSQL
4. Save

#### Error: `OperationalError: could not connect to server`
**Cause**: Database connection issue

**Solution**:
1. Check database is running (Render Dashboard → PostgreSQL)
2. Verify DATABASE_URL format:
   ```
   postgresql://username:password@hostname:port/dbname
   ```
3. Ensure web service and database are in same region
4. Check database allows connections (should be automatic on Render)

---

### 3. Migration Issues

#### Error: `django.db.migrations.exceptions.InconsistentMigrationHistory`
**Cause**: Local migrations don't match production database

**Solution**:
1. **Option A: Fresh Start** (if no important data):
   ```bash
   # In Render Shell
   python manage.py migrate --fake-initial
   ```

2. **Option B: Reset migrations** (if data exists):
   ```bash
   # Backup database first!
   python manage.py migrate --fake
   python manage.py migrate
   ```

#### Error: `No migrations to apply` but tables don't exist
**Solution**:
```bash
# In Render Shell
python manage.py migrate --run-syncdb
```

---

### 4. Static Files Issues

#### Error: Static files not loading (404 errors)
**Cause**: collectstatic not run or WhiteNoise not configured

**Solution**:
1. Check `build.sh` includes:
   ```bash
   python manage.py collectstatic --no-input
   ```
2. Verify `settings_production.py` has:
   ```python
   MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```
3. Manually run in Render Shell:
   ```bash
   python manage.py collectstatic --no-input
   ```

---

### 5. CORS Issues

#### Error in browser: `CORS policy: No 'Access-Control-Allow-Origin' header`
**Cause**: Frontend URL not in CORS allowed origins

**Solution**:
1. Get exact Vercel URL: `https://your-app.vercel.app`
2. Update in Render → Environment:
   ```
   CORS_ALLOWED_ORIGINS=https://your-app.vercel.app
   CSRF_TRUSTED_ORIGINS=https://clinical-case-api.onrender.com,https://your-app.vercel.app
   ```
3. **Important**: No trailing slash, exact match
4. Save and wait for redeploy

#### Error: `CSRF verification failed`
**Cause**: CSRF trusted origins not configured

**Solution**:
Add both frontend and backend URLs:
```
CSRF_TRUSTED_ORIGINS=https://clinical-case-api.onrender.com,https://your-app.vercel.app
```

---

### 6. Environment Variable Issues

#### Error: `KeyError: 'SECRET_KEY'`
**Cause**: SECRET_KEY not set

**Solution**:
1. Generate new key:
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
2. Add to Render Environment variables
3. Or click "Generate" button in Render for SECRET_KEY

---

## Frontend Issues (Vercel)

### 1. Build Errors

#### Error: `Command "npm run build" exited with 1`
**Cause**: Build errors in code

**Solution**:
1. Test locally first:
   ```bash
   cd frontend
   npm install
   npm run build
   ```
2. Fix any TypeScript/ESLint errors
3. Push to GitHub
4. Vercel will auto-redeploy

#### Error: `Cannot find module '@/components/xxx'`
**Cause**: Missing file or incorrect path

**Solution**:
1. Check file exists
2. Verify path alias in `vite.config.ts`:
   ```typescript
   resolve: {
     alias: {
       '@': path.resolve(__dirname, './src')
     }
   }
   ```
3. Check import paths use `@/` prefix

---

### 2. Runtime Errors

#### Error: `Failed to fetch` or `Network Error`
**Cause**: Backend API not accessible

**Solution**:
1. Check `VITE_API_URL` environment variable in Vercel
2. Verify backend is running: `curl https://clinical-case-api.onrender.com/api/health/`
3. Check browser console for exact error
4. Verify CORS is configured on backend

#### Error: API calls return 404
**Cause**: Incorrect API URL or route

**Solution**:
1. Check `VITE_API_URL` doesn't have trailing `/api`:
   ```
   ✅ Correct: https://clinical-case-api.onrender.com
   ❌ Wrong: https://clinical-case-api.onrender.com/api
   ```
2. API base URL should be just the domain

---

### 3. Routing Issues

#### Error: 404 on page refresh
**Cause**: SPA routing not configured

**Solution**:
- Already fixed in `vercel.json` ✅:
  ```json
  "rewrites": [
    { "source": "/(.*)", "destination": "/" }
  ]
  ```

---

### 4. Environment Variables

#### Error: `import.meta.env.VITE_API_URL is undefined`
**Cause**: Environment variable not set in Vercel

**Solution**:
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add:
   ```
   Name: VITE_API_URL
   Value: https://clinical-case-api.onrender.com
   Environment: Production
   ```
3. Redeploy:
   ```bash
   # From Vercel dashboard
   Deployments → Latest → ⋯ → Redeploy
   ```

---

## Database Issues

### 1. Connection Pool Exhausted

#### Error: `OperationalError: connection pool exhausted`
**Cause**: Too many open connections

**Solution**:
In `settings_production.py`:
```python
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,  # Reuse connections
        conn_health_checks=True,  # Check connection health
    )
}
```

---

### 2. Database Full

#### Error: `disk quota exceeded`
**Cause**: Free tier only has 1GB

**Solution**:
1. Upgrade to Starter plan ($7/month, 10GB)
2. Or clean up old data:
   ```python
   # Delete old cases
   Case.objects.filter(created_at__lt=some_date).delete()
   ```

---

### 3. Slow Queries

#### Issue: Slow response times

**Solution**:
1. Add database indexes (already done for common queries)
2. Use `select_related()` and `prefetch_related()`:
   ```python
   cases = Case.objects.select_related('student', 'repository').all()
   ```
3. Consider upgrading to Render PostgreSQL Pro
4. Add Redis caching (advanced)

---

## Performance Issues

### 1. Slow Backend Response (Cold Starts)

#### Issue: First request takes 30+ seconds
**Cause**: Render Free tier spins down after 15 min inactivity

**Solution**:
- **Free option**: Accept cold starts
- **Paid option**: Upgrade to Starter ($7/month) - always on
- **Workaround**: Set up UptimeRobot to ping health endpoint every 10 min

---

### 2. Slow Frontend Loading

#### Issue: Initial page load slow

**Solution**:
1. Check bundle size:
   ```bash
   npm run build -- --mode analyze
   ```
2. Optimize images (use WebP)
3. Add lazy loading for routes
4. Enable Vercel Analytics (free)

---

## Monitoring & Debugging

### View Backend Logs (Render)

```bash
# In Render Dashboard
Your Service → Logs (live tail)

# Or download logs
Your Service → Logs → Download
```

### View Frontend Logs (Vercel)

```bash
# In Vercel Dashboard
Your Project → Deployments → [Latest] → View Function Logs

# Or use CLI
vercel logs
```

### Check Database Status (Render)

```bash
# In Render Dashboard
Your PostgreSQL → Info (see connection count, storage usage)
Your PostgreSQL → Metrics (CPU, memory, connections)
```

---

## Health Check Commands

### Backend Health
```bash
curl https://clinical-case-api.onrender.com/api/health/
# Should return: {"status": "healthy", ...}
```

### Database Connection
```bash
# From Render Shell
python manage.py dbshell
\dt  # List tables
\q   # Exit
```

### Frontend Build
```bash
cd frontend
npm run build
# Should complete without errors
```

---

## Emergency Procedures

### 1. Complete Backend Failure

**Quick Fix**:
1. Render Dashboard → Your Service → Manual Deploy → Deploy latest commit
2. Check logs for errors
3. Verify environment variables
4. If needed, rollback: Deploys → Previous Deploy → Rollback to this version

### 2. Database Corruption

**Recovery**:
1. Render Dashboard → PostgreSQL → Backups
2. Restore from latest backup
3. If no backup, reset database:
   ```bash
   python manage.py flush  # DANGER: Deletes all data
   python manage.py migrate
   python manage.py createsuperuser
   ```

### 3. Can't Access Admin Panel

**Solution**:
```bash
# Create new superuser in Render Shell
python manage.py createsuperuser

# Or reset existing user password
python manage.py changepassword username
```

---

## Getting Help

### 1. Check Logs First
- Backend: Render → Logs
- Frontend: Vercel → Logs
- Browser: DevTools → Console & Network tab

### 2. Common Commands

**Render Shell**:
```bash
# Access shell
# Render Dashboard → Your Service → Shell

# Common Django commands
python manage.py showmigrations  # Check migrations
python manage.py check           # System check
python manage.py dbshell         # Database shell
python manage.py shell           # Django shell
```

**Local Testing**:
```bash
# Test with production settings
cd backend
export DJANGO_SETTINGS_MODULE=clinical_case_platform.settings_production
export DEBUG=True  # Temporarily for testing
export DATABASE_URL=postgresql://...
python manage.py runserver
```

### 3. Support Resources
- Render Community: https://community.render.com/
- Vercel Docs: https://vercel.com/docs
- Django Deployment: https://docs.djangoproject.com/en/5.0/howto/deployment/

---

## Checklist Before Asking for Help

- [ ] Checked logs (Render & Vercel)
- [ ] Verified environment variables
- [ ] Tested health endpoint
- [ ] Checked CORS configuration
- [ ] Verified database connection
- [ ] Tested locally with same settings
- [ ] Checked browser console for errors
- [ ] Reviewed recent code changes
- [ ] Tried redeploying
- [ ] Searched error message online

---

## Contact Information

**Project Maintainer**: [Your Name]  
**Issue Tracker**: [GitHub Issues URL]  
**Documentation**: See DEPLOYMENT_GUIDE.md

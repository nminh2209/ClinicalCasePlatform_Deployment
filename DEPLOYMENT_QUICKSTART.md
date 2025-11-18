# Quick Deployment Reference

## 🚀 Step-by-Step Deployment

### Prerequisites
- [ ] GitHub account created
- [ ] Render account created (render.com)
- [ ] Vercel account created (vercel.com)
- [ ] Code pushed to GitHub

---

## Part 1: Database (5 minutes)

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **New PostgreSQL**:
   - Click "New +" → "PostgreSQL"
   - Name: `clinical-case-db`
   - Region: Singapore (or closest)
   - Plan: Free
   - Click "Create Database"
3. **Save credentials** (from "Info" tab):
   - Copy "Internal Database URL"

---

## Part 2: Backend (10 minutes)

1. **Push code to GitHub** (if not already):
   ```bash
   cd d:\Download\randoms\HN2.1ProjectA-develop\HN2.1ProjectA-develop
   git add .
   git commit -m "Production deployment setup"
   git push origin main
   ```

2. **Create Web Service on Render**:
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Select your repo
   
3. **Configure**:
   ```
   Name: clinical-case-api
   Region: Singapore (same as database)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: ./build.sh
   Start Command: gunicorn clinical_case_platform.wsgi:application
   Plan: Free
   ```

4. **Add Environment Variables**:
   ```
   DJANGO_SETTINGS_MODULE = clinical_case_platform.settings_production
   SECRET_KEY = [Click "Generate" button]
   DATABASE_URL = [Link to your PostgreSQL database]
   DEBUG = False
   ALLOWED_HOSTS = clinical-case-api.onrender.com
   CORS_ALLOWED_ORIGINS = https://your-app.vercel.app
   ```

5. **Deploy**: Click "Create Web Service"
6. **Wait 5-10 minutes** for build
7. **Verify**: Visit `https://clinical-case-api.onrender.com/api/health/`

8. **Create superuser**:
   - In Render dashboard → Your service → "Shell"
   - Run:
     ```bash
     python manage.py createsuperuser
     ```

---

## Part 3: Frontend (5 minutes)

### Method 1: Vercel Dashboard (Easier)

1. **Login to Vercel**: https://vercel.com/login
2. **Import Project**:
   - Click "Add New" → "Project"
   - Select your GitHub repository
   
3. **Configure**:
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```

4. **Environment Variables**:
   - Click "Environment Variables"
   - Add:
     ```
     VITE_API_URL = https://clinical-case-api.onrender.com
     ```

5. **Deploy**: Click "Deploy"
6. **Wait 2-3 minutes**
7. **Copy your Vercel URL**: `https://your-app.vercel.app`

8. **Update Backend CORS** (Important!):
   - Go back to Render dashboard
   - Your service → "Environment"
   - Update:
     ```
     CORS_ALLOWED_ORIGINS = https://your-app.vercel.app
     CSRF_TRUSTED_ORIGINS = https://clinical-case-api.onrender.com,https://your-app.vercel.app
     ```
   - Click "Save Changes"
   - Service will auto-redeploy

### Method 2: Vercel CLI

```bash
npm install -g vercel
cd frontend
vercel login
vercel --prod

# Set environment variable
vercel env add VITE_API_URL production
# Enter: https://clinical-case-api.onrender.com

# Redeploy
vercel --prod
```

---

## 📝 Testing Checklist

1. **Backend Health**:
   ```bash
   curl https://clinical-case-api.onrender.com/api/health/
   # Should return: {"status": "healthy", ...}
   ```

2. **Frontend loads**: Visit your Vercel URL

3. **Login works**: 
   - Use superuser credentials created earlier
   - Check browser console for CORS errors (should be none)

4. **Create a test case**: Verify database connection

5. **Publish to feed**: Test social feed feature

---

## 🔧 Quick Fixes

### "DisallowedHost" Error
→ Add your URL to `ALLOWED_HOSTS` in Render environment variables

### CORS Error in Browser Console
→ Check `CORS_ALLOWED_ORIGINS` includes your Vercel URL exactly

### Database Connection Error
→ Verify `DATABASE_URL` is linked to PostgreSQL in Render

### 502 Bad Gateway
→ Check Render logs for Python errors

### Build Failed
→ Check Render logs, ensure `build.sh` has execute permission

---

## 📊 Your URLs

After deployment, save these:

```
Frontend: https://your-app.vercel.app
Backend API: https://clinical-case-api.onrender.com
Admin Panel: https://clinical-case-api.onrender.com/admin/
API Docs: https://clinical-case-api.onrender.com/api/docs/
Health Check: https://clinical-case-api.onrender.com/api/health/
Database: [Internal on Render]
```

---

## 💰 Cost

**Free Tier** (Good for testing):
- Vercel: $0
- Render PostgreSQL: $0 (90 days)
- Render Web Service: $0 (spins down after 15min)

**Paid Tier** (Recommended for production):
- Vercel: $0 (hobby is enough)
- Render PostgreSQL: $7/month (always-on, 10GB)
- Render Web Service: $7/month (always-on, no cold starts)
- **Total: $14/month**

---

## 🆘 Support

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Check Logs**:
  - Render: Dashboard → Your Service → "Logs"
  - Vercel: Dashboard → Your Project → Deployments → Latest → "View Function Logs"

---

## 🎯 After Deployment

1. **Test all features thoroughly**
2. **Set up backups** (Render auto-backs up on paid plan)
3. **Add custom domain** (optional)
4. **Configure monitoring** (Render has built-in alerts)
5. **Set up staging environment** (optional)

---

**Total Time**: ~20-30 minutes for first deployment

**Status**: 
- [ ] Database created
- [ ] Backend deployed
- [ ] Frontend deployed
- [ ] Superuser created
- [ ] CORS configured
- [ ] All features tested

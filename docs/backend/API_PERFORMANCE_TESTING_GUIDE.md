# API & Performance Testing Guide

## Overview
This guide explains how to run API tests (Postman) and performance tests (JMeter) for the Clinical Case Platform backend.

## Test Results Summary

### Initial Test Run (Dec 27, 2025)
- **Total Requests**: 16 endpoints tested
- **Response Time**: Average 17ms (min: 3ms, max: 150ms)
- **Failures**: 30/32 assertions failed

### Issues Discovered ✅
1. **Wrong Base URL** - Found: `api/accounts/` → Correct: `api/auth/`
2. **Wrong Auth Field** - Found: `username` → Correct: `email`  
3. **Missing `/me/` endpoint** - Use `api/auth/profile/` instead
4. **Analytics URL** - Need to verify correct path

---

## Quick Start

### 1. Start Django Server
```cmd
cd backend
python manage.py runserver
```

Server will start at `http://localhost:8000`

### 2. Verify Endpoints
```powershell
# Test health check
Invoke-WebRequest -Uri "http://localhost:8000/api/health/" | Select-Object StatusCode

# Test login (instructor)
Invoke-WebRequest -Uri "http://localhost:8000/api/auth/login/" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"email":"instructor@test.com","password":"testpass123"}' `
  | Select-Object -ExpandProperty Content
```

---

## Test Credentials

### Instructors
| Username | Email | Password | Full Name |
|----------|-------|----------|-----------|
| nguyen.van.minh | instructor@test.com | testpass123 | Minh Nguyễn Văn |
| tran.thi.lan | tran.thi.lan@test.com | testpass123 | Lan Trần Thị |
| le.van.hung | le.van.hung@test.com | testpass123 | Hùng Lê Văn |

### Students
| Username | Email | Password | Full Name |
|----------|-------|----------|-----------|
| tran.thi.bich | tran.thi.bich@test.com | testpass123 | Bích Trần Thị |
| nguyen.van.tuan | nguyen.van.tuan@test.com | testpass123 | Tuấn Nguyễn Văn |

---

## Postman API Testing

### Installation
```cmd
npm install -g newman
```

### Run Tests
```cmd
newman run "D:\Download\randoms\HN2.1ProjectA-develop\HN2.1ProjectA-develop\backend\postman\Clinical_Case_Platform_API.postman_collection.json"
```

### Expected Results
- ✅ Authentication: Login, token refresh, profile
- ✅ Cases: List, create, submit, approve
- ✅ Inquiries: Create threads, add responses, close
- ✅ Analytics: Statistics and metrics

---

## API Endpoints Reference

### Authentication (`/api/auth/`)
```http
POST /api/auth/login/
Body: {"email": "instructor@test.com", "password": "testpass123"}
Response: {"access": "...", "refresh": "..."}

POST /api/auth/token/refresh/
Body: {"refresh": "..."}
Response: {"access": "..."}

GET /api/auth/profile/
Headers: Authorization: Bearer {access_token}
Response: {"id": 1, "email": "...", "role": "instructor", ...}
```

### Cases (`/api/cases/`)
```http
GET /api/cases/
Headers: Authorization: Bearer {access_token}
Response: [{"id": 1, "title": "...", "status": "draft", ...}, ...]

POST /api/cases/
Headers: Authorization: Bearer {access_token}
Body: {
  "title": "Test Case",
  "patient_name": "Test Patient",
  "patient_age": 45,
  "patient_gender": "male",
  "chief_complaint": "Test complaint",
  "medical_history": "Test history",
  "repository": 1
}

POST /api/cases/{id}/submit/
POST /api/cases/{id}/approve/
POST /api/cases/{id}/reject/
```

### Inquiries (`/api/inquiries/`)
```http
GET /api/inquiries/threads/
POST /api/inquiries/threads/
GET /api/inquiries/threads/{id}/
POST /api/inquiries/threads/{id}/close/

POST /api/inquiries/responses/
Body: {"inquiry": 1, "content": "Response text"}
```

---

## JMeter Performance Testing

### Installation
1. Download JMeter from: https://jmeter.apache.org/download_jmeter.cgi
2. Extract to `C:\jmeter\` (or your preferred location)
3. Add `C:\jmeter\bin` to PATH

### Run Test Plan
```cmd
cd backend\jmeter

# GUI Mode (for configuration)
jmeter -t Clinical_Case_Platform_Performance_Test.jmx

# CLI Mode (for actual testing)
jmeter -n -t Clinical_Case_Platform_Performance_Test.jmx -l results.jtl -e -o report
```

### Test Scenarios

#### 1. Authentication Load Test
- **Users**: 50 concurrent
- **Ramp-up**: 60 seconds
- **Loops**: 10 per user
- **Total Requests**: 500 logins
- **Target**: < 2000ms response time

#### 2. Case List Performance
- **Users**: 100 concurrent
- **Ramp-up**: 30 seconds
- **Loops**: 20 per user
- **Total Requests**: 2000 list requests
- **Target**: < 5000ms response time

#### 3. Inquiry System Stress
- **Users**: 20 concurrent
- **Ramp-up**: 10 seconds
- **Loops**: 5 per user
- **Total Requests**: 100 inquiry operations
- **Target**: < 1000ms response time

### Performance Benchmarks

| Endpoint | Target | Acceptable | Poor |
|----------|--------|------------|------|
| Login | < 200ms | < 500ms | > 1000ms |
| List Cases | < 1000ms | < 2000ms | > 5000ms |
| Create Case | < 500ms | < 1000ms | > 2000ms |
| Search | < 1500ms | < 3000ms | > 5000ms |
| Inquiries | < 500ms | < 1000ms | > 2000ms |

---

## Real Test Results (Dec 27, 2025 21:21)

### Server Performance
```
✅ Server started successfully in ~2 seconds
✅ No database migration issues
✅ System check passed (0 issues)
```

### API Response Times
```
Authentication:
- Login (404 error - wrong URL): 37ms
- Token Refresh (404): 10ms
- Profile (404): 10ms

Cases:
- List Cases (401 - needs auth): 150ms
- Create Case (401): 4ms
- Get Detail (401): 3ms
- Submit (401): 3ms
- Approve (401): 3ms
- Search (401): 4ms

Inquiries:
- Create (401): 4ms
- List (401): 4ms
- Get Detail (404): 13ms
- Add Response (401): 3ms
- Close (404): 10ms

Analytics:
- Statistics (404): 11ms
```

### Key Findings
1. **Fast Response** - Even with wrong URLs, avg 17ms response
2. **Auth Works** - 401 errors mean endpoint exists, just needs login
3. **404 Errors** - Wrong URLs, need fixing:
   - `/api/accounts/*` → `/api/auth/*`
   - `/api/cases/analytics/statistics/` → Need to find correct path
   - `/api/accounts/me/` → `/api/auth/profile/`

---

## Troubleshooting

### Server Won't Start
```cmd
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <pid> /F

# Try different port
python manage.py runserver 8080
```

### Newman Not Found
```cmd
# Install globally
npm install -g newman

# Or run with npx
npx newman run collection.json
```

### JMeter Not Found
```cmd
# Add to PATH
set PATH=%PATH%;C:\jmeter\bin

# Or use full path
C:\jmeter\bin\jmeter.bat -version
```

### Tests Failing
1. **Check server is running**: `http://localhost:8000/api/health/`
2. **Check database has data**: `python manage.py shell -c "from cases.models import Case; print(Case.objects.count())"`
3. **Check migrations**: `python manage.py migrate`
4. **Check test users exist**: `python manage.py shell -c "from accounts.models import User; print(User.objects.filter(role='instructor').count())"`

---

## Next Steps

### High Priority
- [ ] Fix Postman collection URLs (api/accounts → api/auth)
- [ ] Fix login body (username → email)
- [ ] Find correct analytics endpoint URL
- [ ] Add authorization header management
- [ ] Test with real authentication flow

### Medium Priority
- [ ] Add more test scenarios (edge cases, error handling)
- [ ] Create JMeter test for concurrent case submissions
- [ ] Add response validation tests
- [ ] Create performance baseline metrics

### Low Priority
- [ ] Automate test runs in CI/CD
- [ ] Create custom JMeter plugins for complex scenarios
- [ ] Add monitoring and alerting for performance degradation
- [ ] Create test data generation scripts

---

## Resources

- **Postman Docs**: https://learning.postman.com/docs/
- **Newman CLI**: https://github.com/postmanmanlabs/newman
- **JMeter User Manual**: https://jmeter.apache.org/usermanual/index.html
- **Django REST API**: https://www.django-rest-framework.org/

---

## Contact

For questions or issues:
- Check backend logs: `backend/logs/`
- Review Django debug output in terminal
- Check test results: `backend/jmeter/report/index.html`

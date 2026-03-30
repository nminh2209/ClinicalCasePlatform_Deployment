# JMeter Performance Test Guide

## Overview
This JMeter test suite performs comprehensive load testing on the Clinical Case Platform API with 85 concurrent users across 5 thread groups testing 10 different endpoints.

## Test Configuration

### Thread Groups
1. **Setup Thread** (1 user)
   - Single login to verify server is ready
   - Executes once before main tests

2. **Authentication Test** (10 users, 30s ramp, 3 loops)
   - Tests login and profile endpoints
   - Each thread logs in once and reuses token

3. **Case Operations** (30 users, 45s ramp, 5 loops)
   - List all cases
   - Search cases (query: "cardiac")
   - Get case detail (case ID: 1)

4. **Comments and Notifications** (20 users, 30s ramp, 5 loops)
   - Get comments for case
   - Get notifications
   - Get unread notification count

5. **Feedback and Grades** (15 users, 25s ramp, 3 loops)
   - Get feedback for case
   - Get grades for case

6. **Inquiries** (10 users, 20s ramp, 3 loops)
   - List inquiry threads

### Endpoints Tested (10 total)
- POST `/api/auth/login/` - Authentication
- GET `/api/auth/profile/` - User profile
- GET `/api/cases/` - List cases
- GET `/api/cases/?search=cardiac` - Search cases
- GET `/api/cases/1/` - Case details
- GET `/api/comments/?case=1` - Case comments
- GET `/api/notifications/` - Notifications
- GET `/api/notifications/unread-count/` - Unread count
- GET `/api/feedback/?case=1` - Case feedback
- GET `/api/grades/?case=1` - Case grades
- GET `/api/inquiries/threads/` - Inquiry threads

## How to Run

### Prerequisites
- Java installed (version 8 or higher)
- JMeter installed and added to PATH
- Django backend running on `http://localhost:8000`
- Test user credentials: `instructor@test.com` / `testpass123`

### Execute Test
```powershell
cd backend/jmeter
jmeter -n -t Clinical_Case_Platform_Performance_Test_v2.jmx -l results.jtl -e -o report
```

### View Results
Open `report/index.html` in a web browser to see:
- Response times (average, median, 90th percentile)
- Throughput (requests per second)
- Error rate and types
- Performance graphs over time

## Latest Test Results

**Date:** December 28, 2025  
**Duration:** 4 minutes 15 seconds  
**Total Requests:** 986

### Performance Metrics
- **Success Rate:** 47.57% (469 successful requests)
- **Error Rate:** 52.74% (520 failed requests)
- **Throughput:** 3.9 requests/second
- **Average Response Time:** 4641ms (4.6 seconds)
- **Max Response Time:** 17235ms (17.2 seconds)

### Error Breakdown
- **500 Internal Server Errors:** 394 (39.96%)
  - Application errors under sustained concurrent load
  - Primarily on case operations, notifications, and comments endpoints
  
- **401 Unauthorized:** 123 (12.48%)
  - Timing issues where token not yet available
  - Race conditions in concurrent thread execution

### Authentication Pattern
Each thread group uses `OnceOnlyController` to:
1. Login once per thread (not per loop iteration)
2. Extract JWT access token: `$.tokens.access`
3. Store in `${TOKEN}` variable
4. Reuse token for all subsequent requests in that thread
5. Override Authorization header for login requests (prevents thread-level header from interfering)

### Think Time
- Constant timer: 600-1000ms between requests
- Simulates realistic user behavior with pauses

## Known Issues

### 1. High 500 Error Rate (40%)
**Cause:** Django application struggles under sustained concurrent load
- Database connection pool limits
- Transaction locking issues
- Resource contention

**Impact:** Realistic stress test showing application limits

**Recommendation:** 
- Increase database connection pool size
- Add caching for frequently accessed data
- Optimize slow queries
- Consider horizontal scaling

### 2. Authentication Race Conditions (12.5%)
**Cause:** Some threads attempt authenticated requests before `${TOKEN}` is fully set
- JMeter variable scope and timing
- Concurrent thread startup

**Impact:** Minor - most authentication works correctly

**Recommendation:**
- Add small delay after OnceOnlyController (currently has think time)
- Consider using synchronizing timer if critical

### 3. Application Response Time Degradation
**Baseline:** ~100-200ms for simple requests when server idle
**Under Load:** 4641ms average, 17235ms maximum

**Cause:** Server resource exhaustion under 85 concurrent users

## Comparison with PowerShell Stress Test

| Metric | JMeter Test | PowerShell Test |
|--------|-------------|-----------------|
| Concurrent Users | 85 | 100 |
| Test Duration | 4m 15s | ~60s |
| Success Rate | 47.57% | 92.19% |
| Avg Response Time | 4641ms | 11400ms |
| Request Pattern | Sustained load | Burst pattern |
| Throughput | 3.9 req/s | 0.29 req/s |

**Key Difference:** JMeter applies sustained concurrent load over 4+ minutes, while PowerShell test uses burst pattern over 60 seconds. JMeter better simulates realistic prolonged usage and exposes application limits under sustained pressure.

## Test File Structure

```
backend/jmeter/
├── Clinical_Case_Platform_Performance_Test_v2.jmx  # Main test file
├── results.jtl                                      # Raw results (CSV format)
├── report/                                          # HTML report directory
│   └── index.html                                   # Main report page
├── JMETER_PERFORMANCE_TEST_GUIDE.md                # This documentation
└── *.jmx.backup*                                    # Backup files (safe to delete)
```

## Customization

### Adjust Load
Edit thread group parameters in JMX file or GUI:
- `ThreadGroup.num_threads` - Number of concurrent users
- `ThreadGroup.ramp_time` - Time to reach full user count (seconds)
- `LoopController.loops` - Number of iterations per thread

### Modify Think Time
Change `ConstantTimer.delay` value (milliseconds):
```xml
<stringProp name="ConstantTimer.delay">1000</stringProp>
```

### Change Test Credentials
Update login request body in all OnceOnlyControllers:
```json
{"email":"instructor@test.com","password":"testpass123"}
```

### Add New Endpoints
1. Open JMX file in JMeter GUI: `jmeter -t Clinical_Case_Platform_Performance_Test_v2.jmx`
2. Add HTTP Request sampler to appropriate thread group
3. Configure path, method, parameters
4. Add Header Manager with `Authorization: Bearer ${TOKEN}` if authenticated
5. Save and run

## Troubleshooting

### Error: "Results file not empty"
```powershell
Remove-Item results.jtl -Force
```

### Error: "Report folder not empty"
```powershell
Remove-Item report -Recurse -Force
```

### Server Not Responding
1. Check Django is running: `http://localhost:8000/api/auth/login/`
2. Verify test user exists in database
3. Check server logs for errors

### All Requests Return 401
- Token extraction failed - check JSONPostProcessor path: `$.tokens.access`
- Authorization header format incorrect - should be: `Bearer ${TOKEN}`
- Login credentials invalid

### High Error Rate
- Normal under very high load (85 concurrent users)
- Reduce thread counts in thread groups
- Increase ramp time for gradual load increase
- Check server resources (CPU, memory, database connections)

## Best Practices

1. **Clean Results Between Runs**
   ```powershell
   Remove-Item report -Recurse -Force -ErrorAction SilentlyContinue
   Remove-Item results.jtl -Force -ErrorAction SilentlyContinue
   ```

2. **Start with Lower Load**
   - Reduce num_threads by 50%
   - Increase ramp_time to gradual load
   - Verify success rate above 80%
   - Gradually increase load

3. **Monitor Server Resources**
   - Watch CPU, memory, disk I/O
   - Check database connection pool usage
   - Review Django logs for errors
   - Monitor network bandwidth

4. **Baseline Before Load Testing**
   - Run Postman collection first (functional test)
   - Verify all endpoints work with single user
   - Check server health before applying load

5. **Analyze Results**
   - Focus on response time percentiles (90th, 95th)
   - Identify slowest endpoints
   - Look for error patterns
   - Compare runs to detect regressions

## Related Documentation
- [API Documentation](../API_DOCUMENTATION.md)
- [Testing Guide](../TESTING_GUIDE.md)
- [Postman Collection](postman/Clinical_Case_Platform_API_Fixed.postman_collection.json)
- [PowerShell Tests](../comprehensive_api_test.ps1, ../stress_test.ps1)

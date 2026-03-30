# Redis Setup Guide for Clinical Case Platform

## Overview

Redis is used for **real-time WebSocket notifications** in the Clinical Case Platform. It powers the instant notification system via Django Channels when:

- Instructors create inquiries on student cases
- Users respond to inquiries
- Case status changes
- Comments are added

**Important:** Redis is **optional** for basic functionality. Notifications are always saved to the database. Redis only enables the real-time push notification feature via WebSockets.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Notification Flow                        │
└─────────────────────────────────────────────────────────────┘

Event Trigger (e.g., Inquiry Created)
            ↓
┌───────────────────────────────────┐
│   Django Signal Handler           │
│   (inquiries/signals.py)          │
└───────────────────────────────────┘
            ↓
    ┌───────────────┐
    │ Save to DB    │ ← ALWAYS WORKS (even without Redis)
    │ (Notification │
    │   Model)      │
    └───────────────┘
            ↓
    ┌───────────────────────────────┐
    │  Try Real-Time Push           │
    │  (via Redis + Channels)       │
    └───────────────────────────────┘
            ↓
    If Redis Available:
        ✅ Instant WebSocket notification
    If Redis Unavailable:
        ⚠️  Logged warning, continues normally
        📝 Notification still in DB
        👤 User sees it on next page load
```

## Redis Configuration

### Current Settings

**File:** `backend/clinical_case_platform/settings.py`

```python
# Redis URL (default: localhost:6379)
REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/0")

# Django Channels Layer (WebSocket backend)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
            "capacity": 1500,
            "expiry": 10,
        },
    },
}
```

**Environment Variable (Optional):**
```env
# .env or .env.test
REDIS_URL=redis://localhost:6379/0
```

## Installation Options

### Option 1: Docker (Recommended)

**Start Redis:**
```bash
docker run -d -p 6379:6379 --name redis redis:latest
```

**Stop Redis:**
```bash
docker stop redis
```

**Start existing container:**
```bash
docker start redis
```

**Remove container:**
```bash
docker stop redis
docker rm redis
```

**View logs:**
```bash
docker logs redis -f
```

---

### Option 2: WSL (Windows Subsystem for Linux)

**Install Redis:**
```bash
# Open WSL terminal
wsl

# Update packages
sudo apt update

# Install Redis
sudo apt install redis-server -y
```

**Start Redis:**
```bash
# Start Redis server
redis-server

# Or run in background
sudo service redis-server start
```

**Stop Redis:**
```bash
sudo service redis-server stop
```

**Check status:**
```bash
sudo service redis-server status
```

---

### Option 3: Native Windows

**Download:**
1. Visit: https://github.com/tporadowski/redis/releases
2. Download: `Redis-x64-5.0.14.1.zip` (or latest)
3. Extract to: `C:\Redis\` (or any folder)

**Start Redis:**
```cmd
cd C:\Redis
redis-server.exe
```

**Install as Windows Service (Optional):**
```cmd
cd C:\Redis
redis-server.exe --service-install redis.windows.conf
redis-server.exe --service-start
```

**Stop Service:**
```cmd
redis-server.exe --service-stop
```

---

### Option 4: Chocolatey (Windows Package Manager)

**Install:**
```powershell
# Install Chocolatey first if needed
# Then install Redis
choco install redis-64 -y
```

**Start Redis:**
```powershell
redis-server
```

---

## Verification

### Test Redis Connection

**Method 1: redis-cli**
```bash
redis-cli ping
# Expected output: PONG
```

**Method 2: Python**
```python
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
print(r.ping())  # Should print: True
```

**Method 3: Check Port**
```powershell
# Windows
netstat -an | findstr 6379

# Linux/WSL
netstat -tuln | grep 6379
```

**Method 4: Django Test**
```python
# In Django shell
python manage.py shell

from channels.layers import get_channel_layer
channel_layer = get_channel_layer()
print(channel_layer)  # Should show RedisChannelLayer
```

---

## Testing Without Redis

To verify the system works without Redis:

1. **Stop Redis:**
   ```bash
   docker stop redis
   # or
   sudo service redis-server stop
   ```

2. **Create an inquiry via API:**
   ```bash
   # Should return 201 Created
   # Notification saved to database
   # Warning logged but no error
   ```

3. **Check notification in database:**
   ```python
   python manage.py shell
   from notifications.models import Notification
   Notification.objects.all()
   ```

4. **API still works:**
   - POST `/api/inquiries/threads/` → ✅ 201 Created
   - GET `/api/notifications/` → ✅ Shows notification
   - Only missing: Real-time WebSocket push

---

## Troubleshooting

### Redis Connection Refused

**Error:**
```
ConnectionRefusedError: [WinError 1225] The remote computer refused the network connection
```

**Solution:**
- Redis is not running
- Start Redis using one of the methods above
- Verify with `redis-cli ping`

---

### Port Already in Use

**Error:**
```
Address already in use
```

**Solution:**
```bash
# Find process using port 6379
# Windows:
netstat -ano | findstr 6379
taskkill /PID <process_id> /F

# Linux/WSL:
sudo lsof -ti:6379 | xargs sudo kill -9
```

---

### Docker Redis Not Starting

**Check logs:**
```bash
docker logs redis
```

**Remove and recreate:**
```bash
docker stop redis
docker rm redis
docker run -d -p 6379:6379 --name redis redis:latest
```

---

### WSL Redis Not Accessible from Windows

**Issue:** WSL Redis not accessible from Windows Django

**Solution 1: Port forwarding (WSL2)**
```bash
# In WSL, find IP
hostname -I

# Use that IP in Django settings
REDIS_URL=redis://172.x.x.x:6379/0
```

**Solution 2: Use Docker instead**
```bash
# Docker containers are accessible on localhost
docker run -d -p 6379:6379 --name redis redis:latest
```

---

## Production Considerations

### Security

**Enable password authentication:**
```bash
# Redis config
requirepass your_secure_password
```

**Django settings:**
```python
REDIS_URL = "redis://:your_secure_password@localhost:6379/0"
```

### Performance

**Adjust capacity and expiry:**
```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
            "capacity": 3000,     # Increase for high traffic
            "expiry": 60,         # Longer expiry for reliability
        },
    },
}
```

### Persistence

**Enable Redis persistence (optional):**
```bash
# Redis config
save 900 1      # Save after 900 seconds if at least 1 key changed
save 300 10     # Save after 300 seconds if at least 10 keys changed
save 60 10000   # Save after 60 seconds if at least 10000 keys changed
```

### Monitoring

**Check Redis info:**
```bash
redis-cli info

# Memory usage
redis-cli info memory

# Connected clients
redis-cli info clients
```

---

## Development Workflow

### Standard Workflow (With Redis)

```bash
# Terminal 1: Start Redis
docker run -d -p 6379:6379 --name redis redis:latest

# Terminal 2: Start Django
cd backend
python manage.py runserver

# Terminal 3: Start Frontend
cd frontend
npm run dev

# ✅ Full real-time notifications
```

### Simplified Workflow (Without Redis)

```bash
# Terminal 1: Start Django only
cd backend
python manage.py runserver

# Terminal 2: Start Frontend
cd frontend
npm run dev

# ✅ Basic functionality works
# ⚠️  No real-time push (notifications still saved)
```

---

## Integration with Start Scripts

### Windows Batch Script

**File:** `start_all_with_redis.bat`
```batch
@echo off
echo Starting Redis...
docker start redis || docker run -d -p 6379:6379 --name redis redis:latest
timeout /t 2 /nobreak

echo Starting Backend...
start cmd /k "cd backend && python manage.py runserver"

echo Starting Frontend...
start cmd /k "cd frontend && npm run dev"

echo All services started!
```

### Linux/WSL Script

**File:** `start_all_with_redis.sh`
```bash
#!/bin/bash
echo "Starting Redis..."
docker start redis || docker run -d -p 6379:6379 --name redis redis:latest
sleep 2

echo "Starting Backend..."
cd backend
python manage.py runserver &

echo "Starting Frontend..."
cd ../frontend
npm run dev &

echo "All services started!"
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Start Redis (Docker) | `docker start redis` or `docker run -d -p 6379:6379 --name redis redis:latest` |
| Stop Redis (Docker) | `docker stop redis` |
| Test Redis | `redis-cli ping` |
| View Redis logs | `docker logs redis -f` |
| Django shell test | `python manage.py shell` → `from channels.layers import get_channel_layer` |
| Check Django logs | Look for "Failed to send real-time notification" warnings |

---

## FAQ

**Q: Is Redis required for the application to work?**
A: No. Notifications are saved to the database regardless. Redis only enables instant WebSocket push notifications.

**Q: What happens if Redis goes down in production?**
A: Notifications continue to be saved and displayed. Users just won't get instant push notifications until Redis is back.

**Q: How much memory does Redis need?**
A: For this application, 256MB is sufficient. Default Docker image uses minimal memory.

**Q: Can I use a remote Redis server?**
A: Yes. Update `REDIS_URL` in settings: `redis://remote-server:6379/0`

**Q: Do I need Redis for testing?**
A: No. Tests mock WebSocket notifications. See `backend/TESTING_PROGRESS.md` for details.

---

## Related Documentation

- [Testing Guide](TESTING_GUIDE.md) - How tests handle Redis
- [Notification System](../NOTIFICATION_SYSTEM.md) - Notification architecture
- [Setup Guide](../README_SETUP.md) - General project setup
- [Django Channels Documentation](https://channels.readthedocs.io/) - WebSocket framework

---

## Support

If Redis is causing issues during development, you can:
1. **Work without it** - Basic functionality intact
2. **Check logs** - Django logs show Redis connection attempts
3. **Restart services** - `docker restart redis` often fixes issues
4. **Use WSL/Docker** - More reliable than native Windows Redis

For production deployments, Redis is recommended for the best user experience with real-time notifications.

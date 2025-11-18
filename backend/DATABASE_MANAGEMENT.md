# Database Management Guide

## Overview
This guide covers how to manage the database for the Clinical Case Platform, including clearing old data and creating fresh test data.

---

## 🗑️ Dropping Old Data

### Option 1: Using the Reset Script (RECOMMENDED)
```bash
# Activate virtual environment first
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run the reset script
python reset_database.py
```

This script will:
- ✅ Safely delete all data in correct order (respecting foreign keys)
- ✅ Show you what's being deleted
- ✅ Ask for confirmation before proceeding
- ✅ Optionally repopulate with test data

---

### Option 2: Using Django Management Commands
```bash
# Drop all tables and recreate them
python manage.py flush

# Then recreate migrations (if needed)
python manage.py makemigrations
python manage.py migrate
```

**⚠️ Warning**: `flush` command will delete ALL data permanently!

---

### Option 3: Manual Database Reset (PostgreSQL)
```bash
# Connect to PostgreSQL
psql -U postgres

# Drop the database
DROP DATABASE clinical_case_db;

# Recreate it
CREATE DATABASE clinical_case_db;

# Exit psql
\q

# Run migrations again
python manage.py migrate
```

---

### Option 4: Delete Specific Models (Selective Cleanup)
```python
# In Django shell
python manage.py shell

# Delete specific data
from cases.models import Case
from accounts.models import User

# Delete all cases
Case.objects.all().delete()

# Delete students only
User.objects.filter(role='student').delete()

# Delete cases from specific department
from cases.medical_models import Department
dept = Department.objects.get(code='TIM')
Case.objects.filter(student__department=dept).delete()
```

---

## 📦 Creating Test Data

### Populate Test Data
```bash
# Run the enhanced test data script
python populate_test_data.py
```

This will create:
- 10 Departments with Vietnamese names
- 1 Admin user
- 5 Instructors (across different departments)
- 8 Students (distributed across departments)
- 3 Repositories
- 3 Case Templates
- 6+ Medical Cases with detailed information

### View Created Data
```python
# In Django shell
python manage.py shell

from accounts.models import User
from cases.models import Case
from cases.medical_models import Department

# Check created data
print(f"Departments: {Department.objects.count()}")
print(f"Users: {User.objects.count()}")
print(f"Cases: {Case.objects.count()}")

# List instructors
for instructor in User.objects.filter(role='instructor'):
    print(f"{instructor.email} - {instructor.department.vietnamese_name}")
```

---

## 🔐 Default Login Credentials

### Admin
- Email: `admin@test.com`
- Password: `minh1234minh`

### Instructors (all use password: `testpass123`)
- `instructor@test.com` - Cardiology
- `tran.thi.lan@test.com` - Internal Medicine
- `le.van.hung@test.com` - Surgery
- `pham.thi.hoa@test.com` - Respiratory
- `hoang.van.nam@test.com` - Neurology

### Students (all use password: `testpass123`)
- `student@test.com` - Internal Medicine (SV2024001)
- `nguyen.van.an@student.com` - Cardiology (SV2024002)
- `tran.thi.binh@student.com` - Cardiology (SV2024003)
- `le.van.cuong@student.com` - Internal Medicine (SV2024004)
- `pham.thi.duyen@student.com` - Surgery (SV2024005)
- `hoang.van.dung@student.com` - Respiratory (SV2024006)
- `vo.thi.em@student.com` - Neurology (SV2024007)
- `dao.van.phuc@student.com` - Cardiology (SV2024008)

---

## 🔄 Complete Reset & Repopulate Workflow

```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Reset database (delete all data)
python reset_database.py
# Answer "yes" to both prompts

# 3. Or do it in two steps:
python reset_database.py  # Answer "yes" then "no"
python populate_test_data.py  # Run separately

# 4. Verify data was created
python manage.py shell
>>> from accounts.models import User
>>> User.objects.count()
14  # Should show 14 users (1 admin + 5 instructors + 8 students)
```

---

## 🛠️ Troubleshooting

### Issue: Foreign Key Constraint Errors
```bash
# Solution: Use the reset_database.py script which deletes in correct order
python reset_database.py
```

### Issue: Migration Issues After Reset
```bash
# Reset migrations
python manage.py migrate --fake accounts zero
python manage.py migrate --fake cases zero
python manage.py migrate accounts
python manage.py migrate cases
```

### Issue: Database Connection Errors
```bash
# Check if PostgreSQL is running
# Windows:
services.msc  # Look for PostgreSQL service

# Linux/Mac:
sudo systemctl status postgresql

# Restart if needed
sudo systemctl restart postgresql
```

---

## 📝 Notes

- **reset_database.py** is idempotent - safe to run multiple times
- **populate_test_data.py** is idempotent - will skip existing records
- Always backup production data before resetting
- Test data includes department-based organization for testing filters
- All test users have complete profile information (IDs, phone numbers, etc.)

---

## 🎯 Quick Commands Reference

```bash
# Full reset + repopulate
python reset_database.py

# Just clear database
python manage.py flush

# Create test data only
python populate_test_data.py

# Open Django shell
python manage.py shell

# Create superuser manually
python manage.py createsuperuser
```

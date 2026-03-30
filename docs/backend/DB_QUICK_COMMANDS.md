## 🚀 Quick Commands

### Health Check

```bash
# Run full database health check
python db_health_check.py --all

# Check only migrations
python db_health_check.py --check-migrations

# Check only schema
python db_health_check.py --check-schema

# Get data summary
python db_health_check.py --summary
```

### Database Reset & Population

```bash
# Full reset and populate (WARNING: Destroys all data)
python manage.py flush
python manage.py migrate
python populate_test_data.py

# Or use the batch script
.\reset_db.bat
```

### Population Scripts

```bash
# Populate test data (users, cases, etc.)
python populate_test_data.py

# Clear existing data and repopulate
python populate_test_data.py --clear-existing

# Populate medical terminology
python populate_medical_terms.py

# Populate validation data
python populate_validation_data.py
```

### Migration Management

```bash
# Check migration status
python manage.py showmigrations

# View migration plan
python manage.py migrate --plan

# View SQL for a specific migration
python manage.py sqlmigrate cases 0014

# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Rollback to a specific migration
python manage.py migrate cases 0013
```

## 🔧 Troubleshooting

### Issue: Column Does Not Exist Error

**Symptom:**

```
django.db.utils.ProgrammingError: column cases_case.xxx does not exist
```

**Solution:**

1. Check if migrations are applied:

   ```bash
   python manage.py showmigrations cases
   ```

2. Verify database schema:

   ```bash
   python db_health_check.py --check-schema
   ```

3. If migration is marked as applied but column missing:

   ```bash
   # Check what columns actually exist
   python check_feed_columns.py

   # Apply manual fix if needed
   python fix_feed_columns.py
   ```

### Issue: Migration Conflicts

**Symptom:**

```
Conflicting migrations detected; multiple leaf nodes in the migration graph
```

**Solution:**

1. Create merge migration:

   ```bash
   python manage.py makemigrations --merge
   ```

2. Review and apply:
   ```bash
   python manage.py migrate
   ```

### Issue: Database Out of Sync

**Symptom:**

- Migrations show as applied but schema doesn't match
- Model validation errors

**Solution:**

1. **Option A - Soft Reset (Preserve migrations):**

   ```bash
   python manage.py migrate cases zero  # Rollback cases migrations
   python manage.py migrate cases       # Reapply
   ```

2. **Option B - Hard Reset (Development only!):**

   ```bash
   python manage.py flush              # Clear data
   python manage.py migrate            # Ensure migrations applied
   python populate_test_data.py        # Repopulate
   ```

3. **Option C - Manual Fix:**
   - Use `fix_feed_columns.py` or similar scripts
   - Manually add missing columns via SQL

## 📋 Verification Scripts

### Available Scripts

1. **`db_health_check.py`** - Comprehensive health check

   - Verifies database connection
   - Checks migration status
   - Validates schema
   - Provides data summary

2. **`check_feed_columns.py`** - Verify feed columns exist

   - Lists feed-related columns in cases_case
   - Shows migration status

3. **`verify_database.py`** - Full integrity verification

   - Tests model queries
   - Verifies foreign keys
   - Validates column access
   - Tests case creation

4. **`find_user_table.py`** - Find user model table name

   - Useful for writing SQL scripts

5. **`fix_feed_columns.py`** - Manual column fix
   - Adds missing feed columns if migrations failed

### Running Verifications

```bash
# Quick health check
python db_health_check.py

# Detailed verification
python verify_database.py

# Check specific columns
python check_feed_columns.py
```

## 🎯 Common Tasks

### Task: Add New Test Data

```bash
# Adds data without clearing existing
python populate_test_data.py
```

### Task: Reset and Populate from Scratch

```bash
# Windows
.\reset_db.bat

# Linux/Mac
./reset_db.sh

# Or manually:
python manage.py flush
python manage.py migrate
python populate_test_data.py
python populate_medical_terms.py
```

### Task: Create Admin User

```bash
python manage.py createsuperuser
```

### Task: Check Database Info

```bash
python manage.py dbshell
# Then in psql:
\dt              # List tables
\d cases_case    # Describe table
\du              # List users
```

### Task: Backup Database

```bash
# Backup
pg_dump -h localhost -U your_user -d clinical_case_platform_test > backup_$(date +%Y%m%d).sql

# Restore
psql -h localhost -U your_user -d clinical_case_platform_test < backup_20241130.sql
```

### Task: Export Data to JSON

```bash
# All data
python manage.py dumpdata > full_backup.json

# Specific app
python manage.py dumpdata cases > cases_backup.json

# Exclude certain models
python manage.py dumpdata --exclude auth.permission > backup.json
```

### Task: Import Data from JSON

```bash
python manage.py loaddata backup.json
```

## 🔒 Login Credentials (Test Database)

**Admin:**

- Email: `admin@test.com`
- Password: `minh1234minh`

**Instructors:** (password: `testpass123`)

- `instructor@test.com` - Khoa Tim Mạch
- `tran.thi.lan@test.com` - Khoa Nội
- `le.van.hung@test.com` - Khoa Ngoại
- `pham.thi.hoa@test.com` - Khoa Hô Hấp
- `hoang.van.nam@test.com` - Khoa Thần Kinh

**Students:** (password: `testpass123`)

- `student@test.com` - Khoa Nội
- Plus 60 more (see `populate_test_data.py` output)

## 📊 Database Schema

### Key Tables

- `accounts_user` - User accounts (students, instructors, admins)
- `cases_case` - Clinical cases
- `cases_department` - Hospital departments
- `repositories_repository` - Case repositories
- `templates_casetemplate` - Case templates
- `cases_clinicalhistory` - Clinical history records
- `cases_physicalexamination` - Physical exam records
- `cases_investigations` - Investigation records
- `cases_diagnosismanagement` - Diagnosis & management

### Important Columns in cases_case

Feed-related columns (added by migration 0014):

- `is_published_to_feed` - Boolean, case published to feed
- `published_to_feed_at` - Timestamp, when published
- `published_by_id` - FK to accounts_user, who published
- `feed_visibility` - 'department' or 'university'
- `is_featured` - Boolean, featured case
- `reaction_count` - Integer, total reactions

## 🆘 Emergency Recovery

If database is completely broken:

```bash
# 1. Drop and recreate database (PostgreSQL)
dropdb clinical_case_platform_test
createdb clinical_case_platform_test

# 2. Run migrations
python manage.py migrate

# 3. Populate data
python populate_test_data.py
python populate_medical_terms.py

# 4. Verify
python db_health_check.py --all
```

## 📝 Notes

- Always backup before major operations
- Test migrations in development first
- Use `--fake` carefully (can cause schema mismatches)
- Keep migration files in version control
- Document any manual schema changes
- Run health checks after major changes

## 🔗 Related Documentation

- `DATABASE_MANAGEMENT.md` - General database management
- `DATABASE_FIX_SUMMARY.md` - Recent fix details
- `ANALYTICS_VALIDATION_SETUP.md` - Analytics setup
- `LOGIN_CREDENTIALS.md` - Test credentials

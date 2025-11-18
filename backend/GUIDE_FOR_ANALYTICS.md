# Quick Start Guide - Analytics & Validation Systems

## Quick Setup (5 minutes)

### 1. Run Migrations

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate

python manage.py makemigrations cases
python manage.py migrate
```

### 2. Populate Initial Data

```bash
python populate_validation_data.py
```

This creates:
- 13 validation rules (required fields, length checks, attachments)
- 40+ medical terminology entries


### 3. Generate Initial Analytics

```bash
python manage.py generate_analytics --period daily
```

### 4. Test the System

```bash
# Start server
python manage.py runserver

# In another terminal, test endpoints
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/case-analytics/
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/validation-rules/
```

## Key Features

### Analytics System

**What it does:**
- Tracks case views and engagement
- Monitors student progress and learning streaks
- Provides platform-wide statistics
- Generates department performance reports

**Main endpoints:**
- `GET /api/case-analytics/` - View case metrics
- `GET /api/student-engagement/` - Student progress
- `GET /api/analytics-dashboard/overview/` - Dashboard data
- `POST /api/case-analytics/{id}/record_view/` - Track views

### Validation System

**What it does:**
- Validates cases against configurable rules
- Ensures clinical data completeness
- Manages submission workflow (draft → review → approval)
- Tracks case quality metrics

**Main endpoints:**
- `POST /api/case-validation/validate_case/` - Validate a case
- `GET /api/case-validation/validation_report/` - Get validation report
- `POST /api/submission-workflow/{id}/submit/` - Submit for review
- `POST /api/submission-workflow/{id}/approve/` - Approve case

## Common Tasks

### Track a Case View

```python
# In your view tracking code
from cases.analytics import CaseViewLog, CaseAnalytics

# Create view log
CaseViewLog.objects.create(
    case=case,
    user=request.user,
    time_spent_seconds=120,
    completed=True,
    access_method='direct'
)

# Update analytics
analytics, _ = CaseAnalytics.objects.get_or_create(case=case)
analytics.update_view_metrics(request.user, 120)
```

### Validate a Case

```python
from cases.validation import CaseValidationRule, CaseValidationResult

# Get applicable rules
rules = CaseValidationRule.objects.filter(is_active=True)

# Validate
issues = []
for rule in rules:
    is_valid, error_msg = rule.validate_case(case)
    if not is_valid:
        issues.append({'rule': rule.name, 'message': error_msg})

# Create result
result = CaseValidationResult.objects.create(
    case=case,
    validation_status='passed' if not issues else 'failed',
    validation_issues=issues
)
```

### Submit a Case

```python
from cases.validation import CaseSubmissionWorkflow

# Get or create workflow
workflow, _ = CaseSubmissionWorkflow.objects.get_or_create(case=case)

# Check if can submit
if workflow.can_submit():
    workflow.transition_to('submitted', user=request.user)
    case.case_status = 'submitted'
    case.save()
```

## 📝 Creating Custom Validation Rules

### Example: Require Blood Test for Diabetes Cases

```python
from cases.validation import CaseValidationRule

CaseValidationRule.objects.create(
    name="Yêu cầu xét nghiệm máu cho bệnh đái tháo đường",
    rule_type="attachment_required",
    severity="error",
    target_field="medical_attachments",
    rule_config={"attachment_types": ["blood_test"]},
    applies_to_specialties=["Endocrinology", "Nội tiết"],
    error_message_vi="Ca bệnh đái tháo đường yêu cầu kết quả xét nghiệm máu",
    help_text="Vui lòng tải lên kết quả xét nghiệm đường huyết",
    is_active=True
)
```

### Example: Check Diagnosis Format

```python
CaseValidationRule.objects.create(
    name="Định dạng mã ICD-10",
    rule_type="pattern_match",
    severity="warning",
    target_field="diagnosis_management.icd10_codes",
    rule_config={"pattern": r"[A-Z]\d{2}(\.\d{1,2})?"},
    error_message_vi="Mã ICD-10 không đúng định dạng (VD: I10, E11.9)",
    help_text="Mã ICD-10 nên có dạng chữ cái + số (VD: I10 cho tăng huyết áp)",
    is_active=True
)
```

## 🔄 Automated Tasks

### Daily Analytics Generation (Cron Job)

```bash
# Add to crontab (crontab -e)
0 1 * * * cd /path/to/backend && source venv/bin/activate && python manage.py generate_analytics --period daily >> /var/log/analytics.log 2>&1
```

### Weekly Validation Check

```bash
# Add to crontab
0 2 * * 0 cd /path/to/backend && source venv/bin/activate && python manage.py validate_cases --all >> /var/log/validation.log 2>&1
```

## 🐛 Troubleshooting

### Analytics not showing data

```bash
# Check if analytics exist
python manage.py shell
>>> from cases.analytics import CaseAnalytics
>>> CaseAnalytics.objects.count()

# Generate if missing
python manage.py generate_analytics --period daily
```

### Validation always failing

```bash
# Check active rules
python manage.py shell
>>> from cases.validation import CaseValidationRule
>>> for rule in CaseValidationRule.objects.filter(is_active=True):
...     print(f"{rule.name}: {rule.severity}")

# Disable problematic rule
>>> rule = CaseValidationRule.objects.get(name="...")
>>> rule.is_active = False
>>> rule.save()
```

### Workflow stuck

```bash
# Check workflow status
python manage.py shell
>>> from cases.validation import CaseSubmissionWorkflow
>>> workflow = CaseSubmissionWorkflow.objects.get(case_id=123)
>>> print(workflow.current_status)
>>> print(workflow.workflow_history)

# Force transition (admin only)
>>> workflow.transition_to('approved', user=admin_user, notes="Manual override")
```

## Full Documentation

See `ANALYTICS_VALIDATION_SETUP.md` for:
- Complete API reference
- Detailed examples
- Database schema
- Best practices
- Advanced configuration

## Verification Checklist

- [ ] Migrations completed successfully
- [ ] Validation rules created (check admin panel)
- [ ] Medical terminology populated
- [ ] Analytics generated for today
- [ ] Admin interfaces accessible
- [ ] API endpoints responding
- [ ] Test case validated successfully
- [ ] Workflow transitions working

## Next Steps

1. **Configure validation rules** for your specific needs
2. **Set up cron jobs** for automated analytics
3. **Integrate frontend** with API endpoints
4. **Train users** on submission workflow
5. **Monitor analytics** dashboard regularly

## Tips

- Start with WARNING severity for new rules, change to ERROR after testing
- Use `--help` flag on management commands for all options
- Check Django admin for visual rule management
- Review validation reports before enforcing strict rules
- Generate analytics daily for accurate metrics

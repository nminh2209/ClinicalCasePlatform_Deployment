# Analytics System

## Features

### 1. Case Analytics
- Track views, engagement, and learning outcomes for each case
- Monitor completion rates and average grades
- Analyze case effectiveness

### 2. Student Engagement Metrics
- Track individual student activity and progress
- Monitor learning streaks and study time
- Identify areas for improvement

### 3. Platform Usage Statistics
- System-wide metrics (daily/weekly/monthly)
- User activity tracking
- Resource usage monitoring

### 4. Department Analytics
- Department-level performance metrics
- Comparative analysis across departments

## API Endpoints

### Case Analytics

```bash
# Get case analytics
GET /api/case-analytics/

# Get specific case analytics
GET /api/case-analytics/{id}/

# Record a case view
POST /api/case-analytics/{id}/record_view/
{
  "time_spent_seconds": 120,
  "completed": true,
  "access_method": "direct"
}

# Get top performing cases
GET /api/case-analytics/top_cases/?metric=views&limit=10
```

### Student Engagement

```bash
# Get student engagement metrics
GET /api/student-engagement/

# Get detailed progress report
GET /api/student-engagement/{id}/progress_report/

# Get leaderboard
GET /api/student-engagement/leaderboard/?metric=grade&limit=20
```

### Analytics Dashboard

```bash
# Get dashboard overview
GET /api/analytics-dashboard/overview/

# Get trend data
GET /api/analytics-dashboard/trends/?period=30
```

### Platform Statistics

```bash
# Get platform statistics
GET /api/platform-statistics/

# Generate daily statistics (Admin only)
POST /api/platform-statistics/generate_daily/
```

## Management Commands

### Generate Analytics

```bash
# Generate daily analytics
python manage.py generate_analytics --period daily

# Generate weekly analytics
python manage.py generate_analytics --period weekly

# Generate for specific date
python manage.py generate_analytics --period daily --date 2025-11-10
```

**Recommended**: Set up a cron job to run daily:

```bash
# Add to crontab (crontab -e)
0 1 * * * cd /path/to/backend && source venv/bin/activate && python manage.py generate_analytics --period daily
```

## Usage Examples for FE Team

### Track Case Views (Frontend Integration)

```javascript
// When user views a case
const trackCaseView = async (caseId, timeSpent) => {
  const analyticsId = await getCaseAnalyticsId(caseId);
  
  await fetch(`/api/case-analytics/${analyticsId}/record_view/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      time_spent_seconds: timeSpent,
      completed: true,
      access_method: 'direct',
      device_type: 'desktop'
    })
  });
};
```

### Display Student Progress

```javascript
// Get student progress report
const getStudentProgress = async (studentId) => {
  const response = await fetch(
    `/api/student-engagement/${studentId}/progress_report/`,
    {
      headers: { 'Authorization': `Bearer ${token}` }
    }
  );
  
  const data = await response.json();
  
  // Display metrics
  console.log('Average Grade:', data.engagement_metrics.average_grade);
  console.log('Current Streak:', data.engagement_metrics.current_streak_days);
  console.log('Strengths:', data.strengths);
  console.log('Areas for Improvement:', data.areas_for_improvement);
};
```

# Validation System

## Features

### 1. Configurable Validation Rules
- Required field validation
- Minimum/maximum length checks
- Pattern matching
- Attachment requirements
- Medical terminology verification
- Learning objective validation

### 2. Case Quality Metrics
- Completeness scoring
- Quality assessment
- Attachment evaluation
- Vietnamese language quality

### 3. Submission Workflow
- Draft → Validation → Submission → Review → Approval
- Revision requests
- Rejection handling
- Workflow history tracking

### 4. Medical Terminology Dictionary
- Approved medical terms
- Vietnamese translations
- Category organization

## API Endpoints

### Validation Rules

```bash
# Get validation rules
GET /api/validation-rules/

# Create validation rule (Admin/Instructor)
POST /api/validation-rules/
{
  "name": "Yêu cầu chẩn đoán chính",
  "rule_type": "required_field",
  "severity": "error",
  "target_field": "diagnosis_management.primary_diagnosis",
  "rule_config": {},
  "error_message_vi": "Chẩn đoán chính là bắt buộc",
  "help_text": "Vui lòng nhập chẩn đoán chính cho ca bệnh"
}

# Toggle rule active status
POST /api/validation-rules/{id}/toggle_active/
```

### Case Validation

```bash
# Validate a case
POST /api/case-validation/validate_case/
{
  "case_id": 123,
  "validation_type": "pre_submission"
}

# Bulk validate cases
POST /api/case-validation/bulk_validate/
{
  "case_ids": [1, 2, 3],
  "validation_type": "automatic"
}

# Get validation report
GET /api/case-validation/validation_report/?case_id=123
```

### Submission Workflow

```bash
# Get workflow status
GET /api/submission-workflow/{id}/

# Submit case for review
POST /api/submission-workflow/{id}/submit/

# Assign reviewer (Instructor/Admin)
POST /api/submission-workflow/{id}/assign_reviewer/
{
  "reviewer_id": 5
}

# Approve case (Instructor/Admin)
POST /api/submission-workflow/{id}/approve/
{
  "notes": "Excellent work!"
}

# Request revision (Instructor/Admin)
POST /api/submission-workflow/{id}/request_revision/
{
  "notes": "Please add more details to the diagnosis section"
}

# Reject case (Instructor/Admin)
POST /api/submission-workflow/{id}/reject/
{
  "reason": "Does not meet educational standards"
}
```

### Medical Terminology

```bash
# Get medical terms
GET /api/medical-terminology/

# Search terms
GET /api/medical-terminology/?search=diabetes

# Filter by category
GET /api/medical-terminology/?category=Disease

# Get categories
GET /api/medical-terminology/categories/
```

### Quality Metrics

```bash
# Get quality metrics
GET /api/case-quality-metrics/

# Recalculate metrics
POST /api/case-quality-metrics/{id}/recalculate/
```

## Management Commands

### Validate Cases

```bash
# Validate all cases
python manage.py validate_cases --all

# Validate specific case
python manage.py validate_cases --case-id 123

# Validate cases by status
python manage.py validate_cases --status draft

# Recalculate quality metrics
python manage.py validate_cases --recalculate-quality
```

## Setting Up Validation Rules

### Example: Required Fields

```python
# In Django shell or admin
from cases.validation import CaseValidationRule

# Require chief complaint
CaseValidationRule.objects.create(
    name="Yêu cầu lý do khám",
    rule_type="required_field",
    severity="error",
    target_field="clinical_history.chief_complaint",
    rule_config={},
    error_message_vi="Lý do khám là bắt buộc",
    help_text="Vui lòng nhập lý do chính bệnh nhân đến khám",
    is_active=True
)

# Require minimum diagnosis length
CaseValidationRule.objects.create(
    name="Độ dài chẩn đoán tối thiểu",
    rule_type="min_length",
    severity="warning",
    target_field="diagnosis_management.primary_diagnosis",
    rule_config={"min_length": 10},
    error_message_vi="Chẩn đoán quá ngắn (tối thiểu {min_length} ký tự)",
    help_text="Chẩn đoán nên chi tiết và rõ ràng",
    is_active=True
)

# Require X-ray attachment for respiratory cases
CaseValidationRule.objects.create(
    name="Yêu cầu X-quang cho ca hô hấp",
    rule_type="attachment_required",
    severity="error",
    target_field="medical_attachments",
    rule_config={"attachment_types": ["xray"]},
    applies_to_specialties=["Respiratory", "Hô hấp"],
    error_message_vi="Ca bệnh hô hấp yêu cầu ảnh X-quang",
    help_text="Vui lòng tải lên ảnh X-quang phổi",
    is_active=True
)
```

## Usage Examples for FE Team

### Validate Before Submission (Frontend)

```javascript
// Validate case before allowing submission
const validateCase = async (caseId) => {
  const response = await fetch('/api/case-validation/validate_case/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      case_id: caseId,
      validation_type: 'pre_submission'
    })
  });
  
  const result = await response.json();
  
  if (result.validation_status === 'failed') {
    // Show errors to user
    result.validation_issues.forEach(issue => {
      if (issue.severity === 'error') {
        showError(issue.message, issue.help_text);
      }
    });
    return false;
  }
  
  return true;
};

// Submit case
const submitCase = async (workflowId) => {
  const response = await fetch(
    `/api/submission-workflow/${workflowId}/submit/`,
    {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    }
  );
  
  if (response.ok) {
    showSuccess('Ca bệnh đã được nộp thành công!');
  }
};
```

### Display Validation Report

```javascript
// Get and display validation report
const showValidationReport = async (caseId) => {
  const response = await fetch(
    `/api/case-validation/validation_report/?case_id=${caseId}`,
    {
      headers: { 'Authorization': `Bearer ${token}` }
    }
  );
  
  const report = await response.json();
  
  // Display quality score
  console.log('Overall Score:', report.quality_metrics.overall_quality);
  console.log('Completeness:', report.quality_metrics.overall_completeness);
  
  // Show blocking issues
  if (report.blocking_issues.length > 0) {
    console.log('Blocking Issues:');
    report.blocking_issues.forEach(issue => {
      console.log(`- ${issue.message}`);
    });
  }
  
  // Show warnings
  if (report.warnings.length > 0) {
    console.log('Warnings:');
    report.warnings.forEach(warning => {
      console.log(`- ${warning.message}`);
    });
  }
  
  // Can submit?
  console.log('Can Submit:', report.can_submit);
};
```

# Database Schema

## Analytics Tables

- `cases_caseanalytics` - Case usage and engagement metrics
- `cases_studentengagementmetrics` - Student learning patterns
- `cases_caseviewlog` - Detailed view tracking
- `cases_platformusagestatistics` - System-wide statistics
- `cases_departmentanalytics` - Department-level metrics

## Validation Tables

- `cases_casevalidationrule` - Configurable validation rules
- `cases_casevalidationresult` - Validation results history
- `cases_casesubmissionworkflow` - Submission and review workflow
- `cases_medicalterminologycheck` - Medical terminology dictionary
- `cases_casequalitymetrics` - Quality assessment metrics

# Best Practices

## Analytics

1. **Regular Generation**: Run `generate_analytics` daily via cron job
2. **View Tracking**: Track all case views for accurate metrics
3. **Performance**: Use database indexes for large datasets
4. **Privacy**: Respect student privacy in analytics displays

## Validation

1. **Rule Configuration**: Start with essential rules, add more gradually
2. **Severity Levels**: Use "error" for blocking issues, "warning" for suggestions
3. **Clear Messages**: Provide helpful error messages in Vietnamese
4. **Workflow**: Assign reviewers promptly to avoid bottlenecks
5. **Quality Metrics**: Recalculate regularly for accurate assessments

# Troubleshooting

## Analytics Not Updating

```bash
# Manually trigger analytics generation
python manage.py generate_analytics --period daily

# Check for errors in logs
tail -f backend/logs/django.log
```

## Validation Failing Unexpectedly

```bash
# Check validation rules
python manage.py shell
>>> from cases.validation import CaseValidationRule
>>> rules = CaseValidationRule.objects.filter(is_active=True)
>>> for rule in rules:
...     print(f"{rule.name}: {rule.severity}")

# Validate specific case with details
python manage.py validate_cases --case-id 123
```

## Migration Issues

```bash
# If migrations fail, try:
python manage.py migrate cases --fake-initial

# Or reset migrations (development only!)
python manage.py migrate cases zero
python manage.py migrate cases
```

# Support

For issues or questions:
1. Check Django logs: `backend/logs/django.log`
2. Review validation results in admin panel
3. Run management commands with `--help` flag for options

# Future Enhancements

Potential improvements:
- Machine learning for quality prediction
- Automated terminology extraction
- Real-time analytics dashboard
- Email notifications for workflow events
- Export analytics reports to PDF/Excel
- Advanced search and filtering
- Custom validation rule types
- Integration with external medical databases

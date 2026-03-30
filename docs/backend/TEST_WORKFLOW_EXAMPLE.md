# Test Workflow - Real Example

## Current Test Status

**Coverage:** 29% of cases/views.py (18 tests passing)

### What IS Tested ✅
- Case creation (with auth + validation)
- Case visibility (student vs instructor)
- Submit workflow (draft → submitted)
- Approval workflow (submitted → approved)
- Update restrictions (draft only)
- Delete permissions (owner only)

### Critical Gaps ❌
- Reject workflow (return to draft)
- Clone cases
- File uploads
- Share/permissions
- Search/filtering
- Analytics
- Exports

---

## How to Use Tests During Development

### Scenario 1: You're Adding a Feature

**Before writing code:**
```bash
# Write test first (it will FAIL)
cd backend

# Create test that describes desired behavior
# Example: test_instructor_rejects_case()

# Run it - should FAIL because feature doesn't exist yet
python -m pytest cases/tests/test_views_real.py::test_instructor_rejects_case -v
# FAILED - good! feature not built yet
```

**After writing code:**
```bash
# Run test again
python -m pytest cases/tests/test_views_real.py::test_instructor_rejects_case -v
# PASSED - feature works!

# Run all tests to ensure you didn't break anything
python -m pytest cases/tests/test_views_real.py -v
# 19 passed - all good, commit your code
```

### Scenario 2: You're Fixing a Bug

**User reports:** "When I submit a case without patient_name, it crashes the server"

**Your workflow:**
```bash
# 1. Write test that reproduces bug
def test_submit_case_without_patient_name():
    data = {
        "title": "Test",
        "repository": 1,
        "patient_age": 30,
        # Missing patient_name!
    }
    response = api_client.post('/api/cases/', data)
    
    # Should return 400, not crash
    assert response.status_code == 400
    assert 'patient_name' in response.data

# 2. Run test - it FAILS (server crashes)
python -m pytest cases/tests/ -k "without_patient_name" -v
# Server error 500 - BUG CONFIRMED

# 3. Fix the validation in serializers.py
# Add: patient_name = serializers.CharField(required=True)

# 4. Run test again
python -m pytest cases/tests/ -k "without_patient_name" -v
# PASSED - 400 returned with error message

# 5. Commit both test + fix
git add cases/serializers.py cases/tests/test_views_real.py
git commit -m "Fix: Validate patient_name is required"
```

### Scenario 3: Someone Else Changed Code

**You pull from git:**
```bash
git pull origin main
```

**Before starting work:**
```bash
# Run tests to ensure their changes work on your machine
python -m pytest cases/tests/test_views_real.py -v

# If FAILED - their code broke something!
# If PASSED - safe to start working
```

---

## Real Example: Breaking the Code

Let's demonstrate how tests catch bugs:

### What if someone "optimizes" the approve function?

**Original code (cases/views.py line 693):**
```python
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def approve_case(request, pk):
    if not request.user.is_instructor and not request.user.is_admin_user:
        return Response({"error": "Only instructors can approve"}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    case = Case.objects.get(pk=pk)
    if case.case_status not in ["submitted", "reviewed"]:
        return Response({"error": "Can only approve submitted cases"}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    case.case_status = "approved"
    case.reviewed_by = request.user
    case.reviewed_at = timezone.now()
    case.save()
    return Response({"message": "Case approved"})
```

**"Optimized" code (BUGGY):**
```python
def approve_case(request, pk):
    # Someone removed permission check "to make it faster"
    case = Case.objects.get(pk=pk)
    case.case_status = "approved"  # Removed validation!
    case.save()
    return Response({"message": "Case approved"})
```

**What happens:**

```bash
python -m pytest cases/tests/test_views_real.py -v

FAILED test_student_cannot_approve_case - Students CAN now approve! BUG!
FAILED test_cannot_approve_draft_case - Draft cases CAN be approved! BUG!
FAILED test_instructor_approves_submitted_case - reviewed_by not set! BUG!

3 failed, 15 passed - DO NOT COMMIT THIS CODE
```

**Tests caught 3 bugs before they reached production!**

---

## Measuring Impact

### Without Tests
- Developer changes code
- Deploys to production
- Users report: "Students can approve their own cases!" 
- Emergency hotfix required
- User trust damaged

### With Tests
- Developer changes code
- Runs: `python -m pytest`
- Test fails: "Student approved case - Expected 403, got 200"
- Developer fixes bug BEFORE committing
- Users never see the bug

---

## Quick Commands Reference

```bash
# Run all real tests
python -m pytest cases/tests/test_views_real.py -v

# Run one specific test
python -m pytest cases/tests/test_views_real.py::TestCaseApproval::test_instructor_approves_submitted_case -v

# Run tests matching pattern
python -m pytest -k "approve" -v

# Show coverage
python -m pytest cases/tests/test_views_real.py --cov=cases.views --cov-report=term-missing

# Fast test (stop on first failure)
python -m pytest cases/tests/test_views_real.py -x

# Show print statements
python -m pytest cases/tests/test_views_real.py -v -s
```

---

## Next Steps to Improve Coverage

### Priority 1: Test Reject Workflow
```python
def test_instructor_rejects_case():
    """Test rejection returns case to draft with feedback"""
    # This catches if reject() stops working
```

### Priority 2: Test File Uploads
```python
def test_upload_case_attachment():
    """Test students can upload medical images"""
    # This catches if file handling breaks
```

### Priority 3: Test Search
```python
def test_search_cases_by_diagnosis():
    """Test instructors can find cases by diagnosis"""
    # This catches if search queries break
```

**Each test you write = one more bug category prevented**

---

## Summary

**Q: Do tests cover enough?**  
A: No - only 29% of views.py tested. Critical gaps: reject, clone, upload, search, analytics.

**Q: How to use tests for code changes?**  
A: Run tests before + after changes. If they fail = you broke something. If they pass = features still work.

**Value:** Tests catch bugs BEFORE users do. One hour writing tests saves days fixing production bugs.

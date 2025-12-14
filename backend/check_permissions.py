from cases.models import CasePermission, Case
from accounts.models import User

user = User.objects.get(email='vo.thi.yen@student.com')
dept = user.department_id

print(f"User: {user.get_full_name()}")
print(f"Role: {user.role}")
print(f"Department ID: {dept}")
print()

# Check department-level permissions
dept_perms = CasePermission.objects.filter(
    is_active=True,
    share_type='department',
    target_department_id=dept
)
print(f"Department-shared permissions: {dept_perms.count()}")
for p in dept_perms[:10]:
    print(f"  - Case #{p.case_id}: {p.case.title} (by {p.case.student.get_full_name()})")
print()

# Check public permissions
public_perms = CasePermission.objects.filter(
    is_active=True,
    share_type='public'
)
print(f"Public permissions: {public_perms.count()}")
for p in public_perms[:5]:
    print(f"  - Case #{p.case_id}: {p.case.title}")
print()

# Check user-specific permissions  
user_perms = CasePermission.objects.filter(
    is_active=True,
    user=user
)
print(f"User-specific permissions: {user_perms.count()}")
for p in user_perms[:5]:
    print(f"  - Case #{p.case_id}: {p.case.title}")

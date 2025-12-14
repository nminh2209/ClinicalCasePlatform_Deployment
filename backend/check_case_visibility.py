from cases.models import Case
from accounts.models import User

# Get all cases and their visibility
all_cases = Case.objects.all()
print(f"Total cases in database: {all_cases.count()}\n")

# Get student user
user = User.objects.get(email='vo.thi.yen@student.com')
dept_id = user.department_id

print(f"Checking visibility for: {user.get_full_name()} (dept_id={dept_id})")
print(f"User role: {user.role}\n")

# Check each case
for case in all_cases[:20]:
    visibility = []
    if case.student_id == user.id:
        visibility.append("OWNED")
    if case.is_public:
        visibility.append("PUBLIC")
    if case.student.department_id == dept_id:
        visibility.append(f"SAME_DEPT({dept_id})")
    
    owner = case.student.get_full_name()
    vis_str = ", ".join(visibility) if visibility else "NOT VISIBLE"
    print(f"Case #{case.id:2d}: {case.title[:40]:<40} | Owner: {owner:<20} | {vis_str}")

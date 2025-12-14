from cases.models import Case
from accounts.models import User
from django.db.models import Q, Count
from django.utils import timezone

# Simulate the queryset from CaseListCreateView.get_queryset()
user = User.objects.get(email='vo.thi.yen@student.com')

queryset = Case.objects.annotate(
    comment_count=Count("comments", filter=Q(comments__is_reaction=False))
).select_related(
    "student", "student__department",
    "repository", "repository__department",
    "template"
).prefetch_related(
    "medical_attachments",
    "permissions"
)

# Apply student filtering
if user.is_authenticated and getattr(user, "is_student", False):
    department_id = user.department_id
    permission_active_q = Q(permissions__is_active=True) & (
        Q(permissions__expires_at__isnull=True)
        | Q(permissions__expires_at__gte=timezone.now())
    )
    permission_q = permission_active_q & (
        Q(permissions__user=user)
        | Q(
            permissions__share_type="department",
            permissions__target_department_id=department_id,
        )
        | Q(permissions__share_type="public")
    )

    queryset = queryset.filter(
        Q(student=user) | Q(is_public=True) | permission_q
    ).distinct()

print(f"User: {user.get_full_name()}")
print(f"Query would return: {queryset.count()} cases\n")

for case in queryset[:20]:
    owner = case.student.get_full_name()
    status = case.case_status
    is_owner = "(MINE)" if case.student_id == user.id else ""
    print(f"Case #{case.id:2d}: {case.title[:50]:<50} | {owner:<20} {is_owner}")

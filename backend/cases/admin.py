from django.contrib import admin
from .models import Case, CasePermission


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "student",
        "specialty",
        "case_status",
        "patient_name",
        "patient_age",
        "created_at",
    ]
    list_filter = [
        "case_status",
        "specialty",
        "created_at",
        "student__role",
        "repository__is_public",
    ]
    search_fields = [
        "title",
        "patient_name",
        "keywords",
        "case_summary",
        "student__first_name",
        "student__last_name",
        "student__email",
    ]
    readonly_fields = ["created_at", "updated_at", "submitted_at", "reviewed_at"]

    fieldsets = (
        (
            "Thông tin cơ bản",
            {
                "fields": (
                    "title",
                    "student",
                    "template",
                    "repository",
                    "specialty",
                    "case_status",
                )
            },
        ),
        (
            "Thông tin bệnh nhân",
            {
                "fields": (
                    "patient_name",
                    "patient_age",
                    "patient_gender",
                    "medical_record_number",
                    "admission_date",
                    "discharge_date",
                )
            },
        ),
        (
            "Thông tin bổ sung",
            {
                "fields": (
                    "keywords",
                    "case_summary",
                    "priority_level",
                    "complexity_level",
                )
            },
        ),
        (
            "Thời gian",
            {
                "fields": ("created_at", "updated_at", "submitted_at", "reviewed_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("student", "template", "repository")
        )


@admin.register(CasePermission)
class CasePermissionAdmin(admin.ModelAdmin):
    list_display = [
        "case",
        "user",
        "permission_type",
        "granted_by",
        "granted_at",
        "is_active",
    ]
    list_filter = ["permission_type", "is_active", "granted_at"]
    search_fields = [
        "case__title",
        "user__email",
        "user__first_name",
        "user__last_name",
    ]
    readonly_fields = ["granted_at"]

    def get_queryset(self, request):
        return (
            super().get_queryset(request).select_related("case", "user", "granted_by")
        )


# Import analytics admin
from .analytics_admin import *

# Import validation admin
from .validation_admin import *

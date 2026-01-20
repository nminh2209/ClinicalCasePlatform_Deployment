# cases/admin_specialty.py
"""
Django admin configuration for specialty management
"""

from django.contrib import admin
from .specialty_models import Specialty, CasePriorityLevel, CaseComplexityLevel


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    """Admin interface for managing medical specialties"""
    
    list_display = [
        "name",
        "english_name",
        "is_active",
        "display_order",
        "case_count",
        "created_at",
    ]
    
    list_filter = ["is_active", "created_at"]
    
    search_fields = ["name", "english_name", "description"]
    
    list_editable = ["is_active", "display_order"]
    
    fieldsets = (
        ("Thông tin cơ bản", {
            "fields": ("name", "english_name", "description"),
        }),
        ("Cài đặt hiển thị", {
            "fields": ("is_active", "display_order"),
        }),
    )
    
    def case_count(self, obj):
        """Count number of cases using this specialty"""
        # Note: This will work after migration when Case.specialty becomes ForeignKey
        return obj.cases.count() if hasattr(obj, 'cases') else 0
    
    case_count.short_description = "Số ca bệnh"


@admin.register(CasePriorityLevel)
class CasePriorityLevelAdmin(admin.ModelAdmin):
    """Admin interface for managing priority levels"""
    
    list_display = ["name", "key", "color", "is_active", "display_order"]
    list_filter = ["is_active"]
    search_fields = ["name", "key"]
    list_editable = ["is_active", "display_order", "color"]
    
    fieldsets = (
        ("Thông tin cơ bản", {
            "fields": ("name", "key"),
        }),
        ("Cài đặt hiển thị", {
            "fields": ("color", "is_active", "display_order"),
        }),
    )


@admin.register(CaseComplexityLevel)
class CaseComplexityLevelAdmin(admin.ModelAdmin):
    """Admin interface for managing complexity levels"""
    
    list_display = ["name", "key", "is_active", "display_order"]
    list_filter = ["is_active"]
    search_fields = ["name", "key"]
    list_editable = ["is_active", "display_order"]
    
    fieldsets = (
        ("Thông tin cơ bản", {
            "fields": ("name", "key", "description"),
        }),
        ("Cài đặt hiển thị", {
            "fields": ("is_active", "display_order"),
        }),
    )

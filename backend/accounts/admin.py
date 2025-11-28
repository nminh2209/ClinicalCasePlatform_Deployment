from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Session


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "date_joined",
    ]
    list_filter = ["role", "is_active", "is_staff", "date_joined"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["email"]

    fieldsets = (
        ("Thông tin đăng nhập", {"fields": ("email", "password")}),
        ("Thông tin cá nhân", {"fields": ("first_name", "last_name", "role")}),
        (
            "Quyền hạn",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Thời gian",
            {"fields": ("last_login", "date_joined"), "classes": ("collapse",)},
        ),
    )

    add_fieldsets = (
        (
            "Tạo người dùng mới",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ["user", "session_token", "is_active", "expires_at", "created_at"]
    list_filter = ["is_active", "expires_at", "created_at"]
    search_fields = ["user__email", "session_token"]
    readonly_fields = ["created_at"]

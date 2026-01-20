# inquiries/admin.py

from django.contrib import admin
from .models import Inquiry, InquiryResponse, InquiryAttachment


class InquiryResponseInline(admin.TabularInline):
    model = InquiryResponse
    extra = 0
    readonly_fields = ["created_at"]


class InquiryAttachmentInline(admin.TabularInline):
    model = InquiryAttachment
    extra = 0


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ["title", "case", "instructor", "student", "status", "created_at"]
    list_filter = ["status", "created_at", "topic"]
    search_fields = [
        "title",
        "content",
        "case__title",
        "instructor__email",
        "student__email",
    ]
    inlines = [InquiryResponseInline, InquiryAttachmentInline]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(InquiryResponse)
class InquiryResponseAdmin(admin.ModelAdmin):
    list_display = ["inquiry", "author", "created_at"]
    search_fields = ["content", "author__email", "inquiry__title"]
    inlines = [InquiryAttachmentInline]

# inquiries/serializers.py

from rest_framework import serializers
from .models import Inquiry, InquiryResponse, InquiryAttachment
from accounts.serializers import UserSerializer
import os


# Common validation logic
def validate_file_uploads(files):
    """
    Validate file uploads for inquiries and responses.
    Checks file extensions and size limits.
    """
    ALLOWED_EXTENSIONS = [".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx"]
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    for file in files:
        # Check extension
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise serializers.ValidationError(
                f"File type {ext} not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # Check size
        if file.size > MAX_FILE_SIZE:
            raise serializers.ValidationError(
                f"File {file.name} exceeds maximum size of 10MB"
            )

    return files


class InquiryAttachmentSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore[misc, assignment]
        model = InquiryAttachment
        fields = ["id", "file", "filename", "file_size", "uploaded_at"]
        read_only_fields = ["filename", "file_size", "uploaded_at"]


class InquiryResponseSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)
    author_role = serializers.CharField(source="author.role", read_only=True)
    author_avatar = serializers.URLField(
        source="author.profile_picture_url", read_only=True
    )
    attachments = InquiryAttachmentSerializer(many=True, read_only=True)

    # Write-only field for uploading files during response creation
    files = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )

    class Meta:  # type: ignore[misc, assignment]
        model = InquiryResponse
        fields = [
            "id",
            "inquiry",
            "author",
            "author_name",
            "author_role",
            "author_avatar",
            "content",
            "attachments",
            "files",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["author", "created_at", "updated_at"]

    def validate_files(self, files):
        """Validate file uploads"""
        return validate_file_uploads(files)

    def create(self, validated_data):
        files = validated_data.pop("files", [])
        response = super().create(validated_data)

        # Handle attachments
        for file in files:
            InquiryAttachment.objects.create(response=response, file=file)
        return response


class InquirySerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(
        source="instructor.get_full_name", read_only=True
    )
    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    case_title = serializers.CharField(source="case.title", read_only=True)

    responses = InquiryResponseSerializer(many=True, read_only=True)
    attachments = InquiryAttachmentSerializer(many=True, read_only=True)

    # Write-only field for uploading files during creation
    files = serializers.ListField(
        child=serializers.FileField(
            max_length=100000000, allow_empty_file=False, use_url=False  # 100MB
        ),
        write_only=True,
        required=False,
        max_length=10,  # Max 10 files
    )

    class Meta:  # type: ignore[misc, assignment]
        model = Inquiry
        fields = [
            "id",
            "case",
            "case_title",
            "instructor",
            "instructor_name",
            "student",
            "student_name",
            "title",
            "content",
            "status",
            "topic",
            "responses",
            "attachments",
            "files",
            "created_at",
            "updated_at",
            "response_count",
        ]
        read_only_fields = [
            "instructor",
            "student",
            "created_at",
            "updated_at",
            "response_count",
        ]

    def validate_files(self, files):
        """Validate file uploads"""
        return validate_file_uploads(files)

    def create(self, validated_data):
        files = validated_data.pop("files", [])
        inquiry = super().create(validated_data)

        # Handle attachments
        for file in files:
            InquiryAttachment.objects.create(inquiry=inquiry, file=file)
        return inquiry

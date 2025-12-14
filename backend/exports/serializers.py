from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CaseExport, ExportTemplate, BatchExport
from cases.models import Case

User = get_user_model()


class ExportTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for export templates
    """

    created_by_name = serializers.CharField(
        source="created_by.get_full_name", read_only=True
    )
    template_type_display = serializers.CharField(
        source="get_template_type_display", read_only=True
    )

    class Meta:  # type: ignore[misc, assignment]
        model = ExportTemplate
        fields = [
            "id",
            "name",
            "vietnamese_name",
            "description",
            "template_type",
            "template_type_display",
            # Inclusion settings
            "include_patient_details",
            "include_medical_history",
            "include_examination",
            "include_investigations",
            "include_diagnosis",
            "include_treatment",
            "include_learning_objectives",
            "include_comments",
            "include_attachments",
            "include_grades",
            # Formatting options
            "anonymize_patient",
            "add_watermark",
            "watermark_text",
            "header_text",
            "footer_text",
            "logo_url",
            # Metadata
            "created_by",
            "created_by_name",
            "is_active",
            "is_system_template",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "is_system_template"]

    def validate(self, data):  # type: ignore[attr-defined]
        """Validate template settings"""
        # Ensure watermark text is provided if watermark is enabled
        if data.get("add_watermark") and not data.get("watermark_text"):
            data["watermark_text"] = "CONFIDENTIAL"

        return data


class ExportTemplateListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing templates
    """

    template_type_display = serializers.CharField(
        source="get_template_type_display", read_only=True
    )

    class Meta:  # type: ignore[misc, assignment]
        model = ExportTemplate
        fields = [
            "id",
            "name",
            "vietnamese_name",
            "template_type",
            "template_type_display",
            "is_active",
            "is_system_template",
        ]


class CaseExportSerializer(serializers.ModelSerializer):
    """
    Serializer for case exports with full details
    """

    case_title = serializers.CharField(source="case.title", read_only=True)
    case_id = serializers.IntegerField(source="case.id", read_only=True)
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    export_format_display = serializers.CharField(
        source="get_export_format_display", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    template_name = serializers.CharField(
        source="template_used.name", read_only=True, allow_null=True
    )
    file_url = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    can_download = serializers.SerializerMethodField()

    class Meta:  # type: ignore[misc, assignment]
        model = CaseExport
        fields = [
            "id",
            "case",
            "case_id",
            "case_title",
            "user_name",
            "export_format",
            "export_format_display",
            "status",
            "status_display",
            "file_path",
            "file_url",
            "file_size",
            "file_hash",
            "template_used",
            "template_name",
            "export_settings",
            "exported_at",
            "completed_at",
            "download_count",
            "last_downloaded_at",
            "expires_at",
            "is_expired",
            "can_download",
            "error_message",
            "retry_count",
        ]
        read_only_fields = [
            "id",
            "user",
            "file_path",
            "file_size",
            "file_hash",
            "status",
            "exported_at",
            "completed_at",
            "download_count",
            "last_downloaded_at",
            "error_message",
            "retry_count",
        ]

    def get_file_url(self, obj):
        """Get download URL for the exported file"""
        if obj.file_path and obj.status == CaseExport.ExportStatus.COMPLETED:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.file_path.url)
        return None

    def get_is_expired(self, obj):
        """Check if export has expired"""
        return obj.is_expired()

    def get_can_download(self, obj):
        """Check if user can download this export"""
        request = self.context.get("request")
        if not request or not request.user:
            return False

        # User can download their own exports or if they're admin/instructor
        return (
            obj.user == request.user
            or request.user.role in ["admin", "instructor"]
            or obj.case.student == request.user
        )


class CaseExportListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing exports
    """

    case_title = serializers.CharField(source="case.title", read_only=True)
    export_format_display = serializers.CharField(
        source="get_export_format_display", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:  # type: ignore[misc, assignment]
        model = CaseExport
        fields = [
            "id",
            "case",
            "case_title",
            "export_format",
            "export_format_display",
            "status",
            "status_display",
            "file_size",
            "exported_at",
            "download_count",
            "expires_at",
        ]


class CaseExportCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new exports
    """

    class Meta:  # type: ignore[misc, assignment]
        model = CaseExport
        fields = [
            "case",
            "export_format",
            "template_used",
            "export_settings",
            "expires_at",
        ]

    def validate_case(self, value):
        """Validate user has permission to export this case"""
        request = self.context.get("request")
        if not request:
            raise serializers.ValidationError("Request context is required")

        user = request.user

        # Check if user has permission to export this case
        if user.role == "student":
            if value.student != user:
                raise serializers.ValidationError(
                    "Students can only export their own cases"
                )
        elif user.role == "instructor":
            # Instructors can export cases from their department
            if hasattr(user, "department") and hasattr(value, "repository"):
                # Additional department checks can be added here
                pass
        # Admins can export any case

        return value

    def validate_export_format(self, value):
        """Validate export format"""
        valid_formats = [choice[0] for choice in CaseExport.ExportFormat.choices]
        if value not in valid_formats:
            raise serializers.ValidationError(f"Invalid export format: {value}")
        return value

    def create(self, validated_data):
        """Create export record"""
        request = self.context.get("request")
        validated_data["user"] = request.user  # type: ignore[attr-defined]

        # Get IP address and user agent from request
        if request:
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                validated_data["ip_address"] = x_forwarded_for.split(",")[0]
            else:
                validated_data["ip_address"] = request.META.get("REMOTE_ADDR")

            validated_data["user_agent"] = request.META.get("HTTP_USER_AGENT", "")[:500]

        return super().create(validated_data)


class BatchExportSerializer(serializers.ModelSerializer):
    """
    Serializer for batch exports
    """

    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    export_format_display = serializers.CharField(
        source="get_export_format_display", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    template_name = serializers.CharField(
        source="template_used.name", read_only=True, allow_null=True
    )
    case_titles = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    zip_file_url = serializers.SerializerMethodField()

    class Meta:  # type: ignore[misc, assignment]
        model = BatchExport
        fields = [
            "id",
            "user",
            "user_name",
            "cases",
            "case_titles",
            "export_format",
            "export_format_display",
            "template_used",
            "template_name",
            "batch_name",
            "export_settings",
            "compress_output",
            "status",
            "status_display",
            "total_cases",
            "processed_cases",
            "failed_cases",
            "progress_percentage",
            "zip_file",
            "zip_file_url",
            "zip_file_size",
            "created_at",
            "started_at",
            "completed_at",
            "expires_at",
            "task_id",
            "error_message",
        ]
        read_only_fields = [
            "id",
            "user",
            "status",
            "total_cases",
            "processed_cases",
            "failed_cases",
            "zip_file",
            "zip_file_size",
            "started_at",
            "completed_at",
            "task_id",
            "error_message",
        ]

    def get_case_titles(self, obj):
        """Get list of case titles in batch"""
        return list(obj.cases.values_list("title", flat=True)[:10])  # Limit to 10

    def get_progress_percentage(self, obj):
        """Calculate progress percentage"""
        if obj.total_cases > 0:
            return round((obj.processed_cases / obj.total_cases) * 100, 2)
        return 0

    def get_zip_file_url(self, obj):
        """Get download URL for the ZIP file"""
        if obj.zip_file and obj.status == BatchExport.BatchStatus.COMPLETED:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.zip_file.url)
        return None


class BatchExportCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating batch exports
    """

    case_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, min_length=1, max_length=100
    )

    class Meta:  # type: ignore[misc, assignment]
        model = BatchExport
        fields = [
            "case_ids",
            "export_format",
            "template_used",
            "batch_name",
            "export_settings",
            "compress_output",
            "expires_at",
        ]

    def validate_case_ids(self, value):
        """Validate case IDs"""
        request = self.context.get("request")
        user = request.user  # type: ignore[attr-defined]

        # Check if all cases exist
        cases = Case.objects.filter(id__in=value)
        if cases.count() != len(value):
            raise serializers.ValidationError("Some case IDs are invalid")

        # Check permissions
        if user.role == "student":
            # Students can only export their own cases
            unauthorized_cases = cases.exclude(student=user)
            if unauthorized_cases.exists():
                raise serializers.ValidationError(
                    "You don't have permission to export some of these cases"
                )

        return value

    def create(self, validated_data):
        """Create batch export record"""
        request = self.context.get("request")
        case_ids = validated_data.pop("case_ids")

        # Create batch export
        batch_export = BatchExport.objects.create(
            user=request.user,  # type: ignore[attr-defined]
            export_format=validated_data["export_format"],
            template_used=validated_data.get("template_used"),
            batch_name=validated_data.get("batch_name", ""),
            export_settings=validated_data.get("export_settings", {}),
            compress_output=validated_data.get("compress_output", True),
            expires_at=validated_data.get("expires_at"),
            total_cases=len(case_ids),
        )

        # Add cases to batch
        cases = Case.objects.filter(id__in=case_ids)
        batch_export.cases.set(cases)

        return batch_export


class ExportStatsSerializer(serializers.Serializer):
    """
    Serializer for export statistics
    """

    total_exports = serializers.IntegerField()
    exports_by_format = serializers.DictField()
    exports_by_status = serializers.DictField()
    total_downloads = serializers.IntegerField()
    total_file_size = serializers.IntegerField()
    recent_exports = CaseExportListSerializer(many=True)
    popular_templates = serializers.ListField()


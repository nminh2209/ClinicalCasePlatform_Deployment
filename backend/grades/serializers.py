from rest_framework import serializers
from .models import Grade


class GradeSerializer(serializers.ModelSerializer):
    """
    Serializer for Grade model with proper field definitions
    """

    student_id = serializers.IntegerField(source="case.student.id", read_only=True)
    student_name = serializers.CharField(
        source="case.student.get_full_name", read_only=True
    )
    case_title = serializers.CharField(source="case.title", read_only=True)

    class Meta:  # type: ignore[misc, assignment]
        model = Grade
        fields = [
            "id",
            "case",
            "case_title",
            "student_id",
            "student_name",
            "graded_by",
            "grade_scale",
            "score",
            "letter_grade",
            "clinical_reasoning_score",
            "documentation_score",
            "presentation_score",
            "grading_criteria",
            "evaluation_notes",
            "strengths",
            "weaknesses",
            "recommendations",
            "is_final",
            "graded_at",
            "updated_at",
        ]
        read_only_fields = (
            "graded_by",
            "graded_at",
            "student_id",
            "student_name",
            "case_title",
        )

    def validate_grading_criteria(self, value):
        """
        Validate grading_criteria structure if provided
        Rubric weights: History(25), Examination(25), Differential(20), Treatment(20), Presentation(10)
        """
        if value is not None:
            required_keys = [
                "history",
                "examination",
                "differential",
                "treatment",
                "presentation",
            ]
            max_scores = {
                "history": 25,
                "examination": 25,
                "differential": 20,
                "treatment": 20,
                "presentation": 10,
            }

            if not isinstance(value, dict):
                raise serializers.ValidationError("grading_criteria must be an object")

            # Check all required keys are present and validate ranges
            for key in required_keys:
                if key not in value:
                    raise serializers.ValidationError(
                        f"grading_criteria missing required field: {key}"
                    )

                score = value[key]
                if not isinstance(score, (int, float)):
                    raise serializers.ValidationError(f"{key} must be a number")
                if score < 0 or score > max_scores[key]:
                    raise serializers.ValidationError(
                        f"{key} must be between 0 and {max_scores[key]}"
                    )

            # Validate total doesn't exceed 100
            total = sum(value[key] for key in required_keys)
            if total > 100:
                raise serializers.ValidationError(
                    f"Total rubric score cannot exceed 100 (current: {total})"
                )

        return value


class GradeListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing grades
    """

    student_id = serializers.IntegerField(source="case.student.id", read_only=True)
    student_name = serializers.CharField(
        source="case.student.get_full_name", read_only=True
    )
    case_title = serializers.CharField(source="case.title", read_only=True)
    case_specialty = serializers.CharField(source="case.specialty", read_only=True)

    class Meta:  # type: ignore[misc, assignment]
        model = Grade
        fields = [
            "id",
            "case",
            "case_title",
            "case_specialty",
            "student_id",
            "student_name",
            "score",
            "letter_grade",
            "grading_criteria",
            "is_final",
            "graded_at",
        ]

from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Grade
from .serializers import GradeSerializer, GradeListSerializer


class GradeListCreateView(generics.ListCreateAPIView):
    """
    List grades and create new grades with proper filtering
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter grades based on query parameters
        - ?student=me : Get grades for current user (if student)
        - ?case_id=X : Get grade for specific case
        """
        user = self.request.user
        queryset = Grade.objects.select_related(
            "case", "case__student", "graded_by"
        ).all()

        # Filter by student
        if self.request.query_params.get("student") == "me":
            if user.is_student:  # type: ignore[attr-defined]
                queryset = queryset.filter(case__student=user)
            elif user.is_instructor:  # type: ignore[attr-defined]
                # Instructors get all grades they assigned
                queryset = queryset.filter(graded_by=user)

        # Filter by case_id
        case_id = self.request.query_params.get("case_id")
        if case_id:
            queryset = queryset.filter(case_id=case_id)

        return queryset.order_by("-graded_at")

    def get_serializer_class(self):
        """Use detailed serializer for create, list serializer for list"""
        if self.request.method == "POST":
            return GradeSerializer
        return GradeListSerializer

    def perform_create(self, serializer):
        serializer.save(graded_by=self.request.user)


class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a grade
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GradeSerializer

    def get_queryset(self):
        """Filter based on user role"""
        user = self.request.user
        queryset = Grade.objects.select_related(
            "case", "case__student", "graded_by"
        ).all()

        if user.is_student:  # type: ignore[attr-defined]
            # Students can only see their own grades
            queryset = queryset.filter(case__student=user)
        elif user.is_instructor:  # type: ignore[attr-defined]
            # Instructors can see all grades
            pass

        return queryset

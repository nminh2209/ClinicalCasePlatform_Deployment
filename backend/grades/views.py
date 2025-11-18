from rest_framework import generics, permissions

# from rest_framework.response import Response
from .models import Grade


class GradeListCreateView(generics.ListCreateAPIView):
    """
    List grades and create new grades
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Grade.objects.all()

    def get_serializer_class(self):
        from rest_framework import serializers

        class GradeSerializer(serializers.ModelSerializer):
            class Meta:
                model = Grade
                fields = "__all__"
                read_only_fields = ("graded_by", "graded_at")

        return GradeSerializer

    def perform_create(self, serializer):
        serializer.save(graded_by=self.request.user)


class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a grade
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Grade.objects.all()

    def get_serializer_class(self):
        from rest_framework import serializers

        class GradeSerializer(serializers.ModelSerializer):
            class Meta:
                model = Grade
                fields = "__all__"
                read_only_fields = ("graded_by", "graded_at")

        return GradeSerializer

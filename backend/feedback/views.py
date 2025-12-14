from rest_framework import generics, permissions

# from rest_framework.response import Response
from .models import Feedback


class FeedbackListCreateView(generics.ListCreateAPIView):
    """
    List feedback and create new feedback
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Feedback.objects.all()

    def get_serializer_class(self):
        from rest_framework import serializers

        class FeedbackSerializer(serializers.ModelSerializer):
            class Meta:  # type: ignore[misc, assignment]
                model = Feedback
                fields = "__all__"
                read_only_fields = ("instructor", "created_at", "updated_at")

        return FeedbackSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


class FeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete feedback
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Feedback.objects.all()

    def get_serializer_class(self):
        from rest_framework import serializers

        class FeedbackSerializer(serializers.ModelSerializer):
            class Meta:  # type: ignore[misc, assignment]
                model = Feedback
                fields = "__all__"
                read_only_fields = ("instructor", "created_at", "updated_at")

        return FeedbackSerializer

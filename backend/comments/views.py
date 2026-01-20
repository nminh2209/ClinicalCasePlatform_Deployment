# comments/views.py

from rest_framework import generics, permissions

# from rest_framework.response import Response
from .models import Comment


class CommentListCreateView(generics.ListCreateAPIView):
    """
    List comments and create new comments
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        from rest_framework import serializers

        class CommentSerializer(serializers.ModelSerializer):
            author_name = serializers.CharField(
                source="author.get_full_name", read_only=True
            )
            author_role = serializers.CharField(source="author.role", read_only=True)
            reply_count = serializers.ReadOnlyField()

            class Meta:  # type: ignore[misc, assignment]
                model = Comment
                fields = "__all__"
                read_only_fields = ("author", "created_at", "updated_at")

        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a comment
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        from rest_framework import serializers

        class CommentSerializer(serializers.ModelSerializer):
            author_name = serializers.CharField(
                source="author.get_full_name", read_only=True
            )
            author_role = serializers.CharField(source="author.role", read_only=True)
            reply_count = serializers.ReadOnlyField()

            class Meta:  # type: ignore[misc, assignment]
                model = Comment
                fields = "__all__"
                read_only_fields = ("author", "created_at", "updated_at")

        return CommentSerializer

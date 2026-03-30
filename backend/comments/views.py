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

    def get_queryset(self):
        """
        Filter comments by case if case parameter is provided
        """
        queryset = Comment.objects.all()

        # Filter by case ID
        case_id = self.request.query_params.get("case")
        if case_id:
            queryset = queryset.filter(case_id=case_id)

        # Filter by is_reaction
        is_reaction = self.request.query_params.get("is_reaction")
        if is_reaction is not None:
            is_reaction_bool = is_reaction.lower() in ("true", "1", "yes")
            queryset = queryset.filter(is_reaction=is_reaction_bool)

        return queryset.select_related("author", "case").prefetch_related("replies")

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

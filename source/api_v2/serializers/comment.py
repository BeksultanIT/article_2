from rest_framework import serializers
from webapp.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'article', 'author', 'text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'article', 'author', 'created_at', 'updated_at']



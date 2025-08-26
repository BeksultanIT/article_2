from rest_framework import serializers
from webapp.models import statuses, Tag, Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'status', 'tags', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError('Длина названия должна быть не менее 5 символов.')
        return value

    def validate(self, attrs):
        return super().validate(attrs)


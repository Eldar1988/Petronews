from rest_framework import serializers
from .models import Post


class PostListSerializer(serializers.ModelSerializer):
    """Список новостей"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'image_url', 'image', 'views', 'pub_date', 'slug', 'category')
